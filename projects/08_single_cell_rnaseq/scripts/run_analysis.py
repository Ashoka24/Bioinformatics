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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/raw/filtered_gene_bc_matrices/hg19"))
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--min-genes", type=int, default=200)
    parser.add_argument("--max-genes", type=int, default=6000)
    parser.add_argument("--min-cells", type=int, default=3)
    parser.add_argument("--max-pct-mt", type=float, default=20.0)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

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
        (adata.obs["n_genes_by_counts"] >= args.min_genes)
        & (adata.obs["n_genes_by_counts"] <= args.max_genes)
        & (adata.obs["pct_counts_mt"] <= args.max_pct_mt)
    )
    adata = adata[keep].copy()
    sc.pp.filter_genes(adata, min_cells=args.min_cells)
    filtered_shape = {"cells": int(adata.n_obs), "genes": int(adata.n_vars)}
    if adata.n_obs < 3 or adata.n_vars < 3:
        raise SystemExit("Too few cells or genes remain; review thresholds and input matrix.")

    adata.layers["counts"] = adata.X.copy()
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=min(2000, max(1, adata.n_vars - 1)), flavor="seurat")
    adata.var[adata.var["highly_variable"]].to_csv(args.output / "highly_variable_genes.csv")
    adata = adata[:, adata.var["highly_variable"]].copy()
    sc.pp.scale(adata, max_value=10)
    sc.tl.pca(adata, svd_solver="arpack", random_state=args.seed)
    n_pcs = min(30, max(2, adata.obsm["X_pca"].shape[1] - 1))
    sc.pp.neighbors(adata, n_neighbors=min(15, max(2, adata.n_obs - 1)), n_pcs=n_pcs, random_state=args.seed)
    sc.tl.umap(adata, random_state=args.seed)
    try:
        sc.tl.leiden(adata, resolution=0.8, random_state=args.seed, key_added="leiden")
    except ImportError as exc:
        raise SystemExit("Install project requirements, including python-igraph and leidenalg.") from exc

    sc.tl.rank_genes_groups(adata, groupby="leiden", method="wilcoxon")
    markers = sc.get.rank_genes_groups_df(adata, group=None)
    markers.to_csv(args.output / "marker_genes.csv", index=False)
    sc.pl.umap(adata, color=["leiden"], show=False)
    plt.savefig(figures / "umap_clusters.png", bbox_inches="tight")
    plt.close("all")

    top_genes = markers.groupby("group", sort=True).head(3)["names"].dropna().astype(str).unique().tolist()
    if top_genes:
        sc.pl.umap(adata, color=top_genes[:6], show=False)
        plt.savefig(figures / "umap_marker_genes.png", bbox_inches="tight")
        plt.close("all")
    adata.write_h5ad(args.output / "pbmc3k_processed.h5ad", compression="gzip")

    metadata = {
        "dataset": "10x Genomics 3k PBMCs from a Healthy Donor",
        "dataset_page": "https://www.10xgenomics.com/datasets/3-k-pbm-cells-from-a-healthy-donor-1-standard-1-1-0",
        "python_version": platform.python_version(),
        "scanpy_version": sc.__version__,
        "anndata_version": anndata.__version__,
        "seed": args.seed,
        "parameters": {"min_genes": args.min_genes, "max_genes": args.max_genes,
                       "min_cells": args.min_cells, "max_pct_mt": args.max_pct_mt},
        "input_shape": input_shape,
        "filtered_shape": filtered_shape,
        "interpretation": "Exploratory results; clusters are not clinical findings."
    }
    (args.output / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"input": input_shape, "filtered": filtered_shape, "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
