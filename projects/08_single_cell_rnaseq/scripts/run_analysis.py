#!/usr/bin/env python3
"""Run exploratory Scanpy QC, clustering, and marker ranking on a 10x matrix."""
import argparse
import json
import platform
from pathlib import Path

import anndata
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scanpy as sc

DEFAULT_CONFIG = Path("config/analysis.json")


def load_config(path: Path) -> dict:
    """Load and minimally validate analysis parameters from a JSON config."""
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read config file {path}: {exc}") from exc
    if not isinstance(config, dict):
        raise SystemExit(f"Config must contain a JSON object: {path}")
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--input", type=Path, default=Path("data/raw/filtered_gene_bc_matrices/hg19"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--min-genes", type=int)
    parser.add_argument("--max-genes", type=int)
    parser.add_argument("--min-cells", type=int)
    parser.add_argument("--max-pct-mt", type=float)
    parser.add_argument("--target-sum", type=float)
    parser.add_argument("--n-top-genes", type=int)
    parser.add_argument("--n-pcs", type=int)
    parser.add_argument("--n-neighbors", type=int)
    parser.add_argument("--leiden-resolution", type=float)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()

    config = load_config(args.config)
    params = {
        "min_genes": args.min_genes if args.min_genes is not None else config.get("min_genes_per_cell", 200),
        "max_genes": args.max_genes if args.max_genes is not None else config.get("max_genes_per_cell", 6000),
        "min_cells": args.min_cells if args.min_cells is not None else config.get("min_cells_per_gene", 3),
        "max_pct_mt": args.max_pct_mt if args.max_pct_mt is not None else config.get("max_pct_mt", 20.0),
        "target_sum": args.target_sum if args.target_sum is not None else config.get("target_sum", 10000),
        "n_top_genes": args.n_top_genes if args.n_top_genes is not None else config.get("n_top_genes", 2000),
        "n_pcs": args.n_pcs if args.n_pcs is not None else config.get("n_pcs", 30),
        "n_neighbors": args.n_neighbors if args.n_neighbors is not None else config.get("n_neighbors", 15),
        "leiden_resolution": args.leiden_resolution if args.leiden_resolution is not None else config.get("leiden_resolution", 0.8),
        "seed": args.seed if args.seed is not None else config.get("random_seed", 42),
    }
    if params["min_genes"] < 0 or params["max_genes"] < params["min_genes"]:
        raise SystemExit("Require 0 <= min_genes <= max_genes.")
    if params["min_cells"] < 1 or params["target_sum"] <= 0:
        raise SystemExit("min_cells must be >= 1 and target_sum must be positive.")
    if params["n_top_genes"] < 2 or params["n_pcs"] < 2 or params["n_neighbors"] < 2:
        raise SystemExit("n_top_genes, n_pcs, and n_neighbors must each be >= 2.")
    if not 0 <= params["max_pct_mt"] <= 100 or params["leiden_resolution"] <= 0:
        raise SystemExit("max_pct_mt must be in [0, 100] and leiden_resolution must be positive.")

    args.output.mkdir(parents=True, exist_ok=True)
    figures = args.output / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    sc.settings.verbosity = 2
    sc.settings.set_figure_params(dpi=120, facecolor="white")
    sc.settings.autoshow = False
    sc.settings.autosave = False
    sc.settings.n_jobs = 1

    adata = sc.read_10x_mtx(args.input, var_names="gene_symbols", cache=False)
    adata.var_names_make_unique()
    input_shape = {"cells": int(adata.n_obs), "genes": int(adata.n_vars)}
    names = adata.var_names.astype(str)
    adata.var["mt"] = names.str.upper().str.startswith("MT-")
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)
    adata.obs[["total_counts", "n_genes_by_counts", "pct_counts_mt"]].to_csv(args.output / "qc_metrics.csv")

    sc.pl.violin(adata, ["n_genes_by_counts", "total_counts", "pct_counts_mt"], multi_panel=True, show=False)
    plt.savefig(figures / "qc_violin.png", bbox_inches="tight")
    plt.close("all")

    keep = (
        (adata.obs["n_genes_by_counts"] >= params["min_genes"])
        & (adata.obs["n_genes_by_counts"] <= params["max_genes"])
        & (adata.obs["pct_counts_mt"] <= params["max_pct_mt"])
    )
    adata = adata[keep].copy()
    sc.pp.filter_genes(adata, min_cells=params["min_cells"])
    filtered_shape = {"cells": int(adata.n_obs), "genes": int(adata.n_vars)}
    if adata.n_obs < 3 or adata.n_vars < 3:
        raise SystemExit("Too few cells or genes remain; review thresholds and input matrix.")

    adata.layers["counts"] = adata.X.copy()
    sc.pp.normalize_total(adata, target_sum=params["target_sum"])
    sc.pp.log1p(adata)
    # Preserve normalized log-expression for marker statistics before scaling.
    # Rank genes on this representation, not on z-scored values (which can
    # produce undefined fold changes when exponentiated).
    adata.raw = adata.copy()
    n_top_genes = min(params["n_top_genes"], max(2, adata.n_vars - 1))
    sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, flavor="seurat")
    adata.var[adata.var["highly_variable"]].to_csv(args.output / "highly_variable_genes.csv")
    adata = adata[:, adata.var["highly_variable"]].copy()
    sc.pp.scale(adata, max_value=10)
    sc.tl.pca(adata, svd_solver="arpack", random_state=params["seed"])
    available_pcs = int(adata.obsm["X_pca"].shape[1])
    n_pcs = min(params["n_pcs"], max(2, available_pcs - 1))
    n_neighbors = min(params["n_neighbors"], max(2, adata.n_obs - 1))
    sc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=n_pcs, random_state=params["seed"])
    sc.tl.umap(adata, random_state=params["seed"])
    try:
        sc.tl.leiden(adata, resolution=params["leiden_resolution"], random_state=params["seed"], key_added="leiden")
    except ImportError as exc:
        raise SystemExit("Install project requirements, including python-igraph and leidenalg.") from exc

    sc.tl.rank_genes_groups(adata, groupby="leiden", method="wilcoxon", use_raw=True)
    markers = sc.get.rank_genes_groups_df(adata, group=None)
    markers.to_csv(args.output / "marker_genes.csv", index=False)
    sc.pl.umap(adata, color=["leiden"], show=False)
    plt.savefig(figures / "umap_clusters.png", bbox_inches="tight")
    plt.close("all")

    # Keep labels conservative: these are working interpretations of the
    # observed marker patterns, not reference-mapped or experimentally
    # validated cell identities.
    annotation_notes = {
        "0": ("T-cell-enriched", "CD3D; inspect IL7R, CCR7, CD4 and CD8A before finer labels", "moderate"),
        "1": ("Classical monocyte-like", "LYZ; S100A8; S100A9; FCN1", "high"),
        "2": ("Cytotoxic T/NK-like", "NKG7; GZMA; CCL5; PRF1", "moderate"),
        "3": ("B-cell-like", "CD79A; CD79B; MS4A1; CD74", "high"),
        "4": ("FCGR3A-positive monocyte-like", "FCGR3A; LST1; FCER1G; AIF1", "moderate"),
        "5": ("Dendritic/APC-like; small cluster", "FCER1A; CLEC10A; HLA class II genes", "low"),
        "6": ("Unresolved; possible cell-cycle signal", "KIAA0101; HMGB2; insufficient evidence for a firm label", "low"),
        "7": ("Platelet-associated", "PPBP; PF4; SDPR; GNG11", "moderate"),
        "8": ("Unresolved; very small cluster", "Ribosomal-dominated signature; no clear specific marker pattern", "low"),
    }
    cluster_counts = adata.obs["leiden"].astype(str).value_counts()
    annotation_rows = []
    for cluster in sorted(cluster_counts.index, key=lambda value: int(value)):
        label, evidence, confidence = annotation_notes.get(
            cluster, ("Unannotated", "No manual note supplied; inspect cluster markers", "low")
        )
        annotation_rows.append({
            "cluster": cluster,
            "cell_count": int(cluster_counts[cluster]),
            "working_label": label,
            "marker_evidence_to_review": evidence,
            "confidence": confidence,
            "status": "provisional; verify against marker expression and references",
        })
    import pandas as pd
    pd.DataFrame(annotation_rows).to_csv(args.output / "cluster_annotations.csv", index=False)

    marker_groups = {
        "T cells": ["CD3D", "CD3E", "IL7R", "CCR7", "CD4", "CD8A"],
        "Cytotoxic": ["NKG7", "GNLY", "PRF1", "GZMA"],
        "B cells": ["MS4A1", "CD79A", "CD79B", "CD74"],
        "Monocytes": ["LYZ", "S100A8", "S100A9", "FCN1", "FCGR3A", "LST1"],
        "Dendritic/APC": ["FCER1A", "CLEC10A", "HLA-DRA"],
        "Platelet": ["PPBP", "PF4", "SDPR"],
    }
    present_marker_groups = {
        label: [gene for gene in genes if gene in adata.raw.var_names]
        for label, genes in marker_groups.items()
    }
    present_marker_groups = {label: genes for label, genes in present_marker_groups.items() if genes}
    if present_marker_groups:
        sc.pl.dotplot(
            adata,
            var_names=present_marker_groups,
            groupby="leiden",
            use_raw=True,
            standard_scale="var",
            show=False,
        )
        plt.savefig(figures / "dotplot_canonical_markers.png", bbox_inches="tight")
        plt.close("all")

    top_genes = markers.groupby("group", sort=True).head(3)["names"].dropna().astype(str).unique().tolist()
    if top_genes:
        sc.pl.umap(adata, color=top_genes[:6], show=False)
        plt.savefig(figures / "umap_marker_genes.png", bbox_inches="tight")
        plt.close("all")
    adata.write_h5ad(args.output / "pbmc3k_processed.h5ad", compression="gzip")

    metadata = {
        "dataset": config.get("dataset_name", "10x Genomics 3k PBMCs from a Healthy Donor"),
        "dataset_page": "https://www.10xgenomics.com/datasets/3-k-pbm-cells-from-a-healthy-donor-1-standard-1-1-0",
        "python_version": platform.python_version(),
        "scanpy_version": sc.__version__,
        "anndata_version": anndata.__version__,
        "parameters": params,
        "effective_n_top_genes": n_top_genes,
        "effective_n_pcs": n_pcs,
        "effective_n_neighbors": n_neighbors,
        "input_shape": input_shape,
        "filtered_shape": filtered_shape,
        "interpretation": "Exploratory results; clusters are not clinical findings."
    }
    (args.output / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"input": input_shape, "filtered": filtered_shape, "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
