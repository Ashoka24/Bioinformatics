# Project 08 — Single-Cell RNA-seq Analysis

A reproducible single-cell RNA sequencing workflow using Scanpy and the public 10x Genomics PBMC 3k dataset. This project is being built directly in GitHub; no local execution is required to create the repository structure.

## Objective

Explore PBMC gene-expression data through quality control, normalization, highly variable gene selection, PCA, neighborhood graph construction, UMAP, Leiden clustering, and marker-gene ranking.

## Dataset and provenance

- Dataset: 10x Genomics, 3k PBMCs from a Healthy Donor
- Official page: https://www.10xgenomics.com/datasets/3-k-pbm-cells-from-a-healthy-donor-1-standard-1-1-0
- Expected data: filtered feature-barcode matrix (Matrix Market matrix, barcodes, and genes/features)
- Download with: python scripts/download_data.py
- Downloaded matrices and generated results are excluded from Git.

The downloader uses the commonly used 10x PBMC3k archive endpoint and reports the official dataset page as provenance. Verify the vendor page if the archive URL or file layout changes.

## Workflow

1. Download and extract the public filtered matrix.
2. Validate expected matrix, barcode, and feature files.
3. Calculate cell QC metrics and export QC summaries.
4. Filter cells and genes using configurable thresholds.
5. Load analysis thresholds from `config/analysis.json`; normalize counts, log-transform, and identify highly variable genes.
6. Run scaling, PCA, neighborhood graph, and UMAP.
7. Cluster with Leiden and rank marker genes.
8. Export tables, plots, an AnnData object, and run metadata.

## Quick start

Use Python 3.10 or 3.11 in a supported environment:

    python -m venv .venv
    # Windows: .venv\Scripts\activate
    # macOS/Linux: source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    python scripts/download_data.py
    python scripts/validate_inputs.py --input data/raw/filtered_gene_bc_matrices/hg19
    python scripts/run_analysis.py --config config/analysis.json --input data/raw/filtered_gene_bc_matrices/hg19 --output results

These are reproducibility instructions, not a claim that the analysis has already run. GitHub Actions performs static and unit checks and, on pushes to `main` that touch this project, attempts the complete dataset download and analysis in a cloud runner. The full run uploads generated outputs as a workflow artifact for 14 days; no local machine is required.

## Outputs generated when the workflow is run

- results/qc_metrics.csv
- results/highly_variable_genes.csv
- results/marker_genes.csv
- results/pbmc3k_processed.h5ad
- results/run_metadata.json
- results/figures/qc_violin.png
- results/figures/umap_clusters.png
- results/figures/umap_marker_genes.png

## Validation

    python -m unittest discover -s tests -v
    python scripts/validate_inputs.py --input <matrix-directory>

The validator checks file presence, not matrix content or biological quality. GitHub Actions compiles scripts, validates the JSON configuration, and runs unit tests. Pushes to `main` that touch this project also trigger a cloud analysis job; check the Actions run and artifact before treating the analysis as successful.

## Limitations

- QC cutoffs and dimensionality/clustering settings are read from `config/analysis.json`; command-line options can override individual values. Cutoffs remain dataset-dependent.
- Leiden clusters are not automatically validated cell types.
- UMAP is a visualization, not proof of biological separation.
- Marker genes require multi-marker and reference-based interpretation.
- This is an exploratory portfolio workflow, not a clinical diagnostic pipeline.

## References

- 10x Genomics dataset: https://www.10xgenomics.com/datasets/3-k-pbm-cells-from-a-healthy-donor-1-standard-1-1-0
- Scanpy: https://scanpy.readthedocs.io/
- AnnData: https://anndata.readthedocs.io/
