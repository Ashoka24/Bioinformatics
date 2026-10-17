# Interpreting the scRNA-seq outputs

## Quality control
- Total counts per cell: total observed count signal for a barcode.
- Detected genes per cell: genes with non-zero counts.
- Percent mitochondrial counts: fraction of counts assigned to mitochondrial genes; high values can indicate stressed/damaged cells but thresholds are dataset-dependent.
- Review metric distributions before filtering because strict cutoffs can remove genuine biology.

## Analysis
Library-size normalization and log transformation make expression values more comparable. Highly variable genes capture variation useful for downstream analysis. PCA summarizes major variation; a neighbor graph and UMAP provide a low-dimensional visualization.

## Clusters and markers
Leiden clusters are computational groups, not automatically validated cell types. Marker rankings should be interpreted with multiple markers, reference atlases, and biological knowledge. Batch effects, ambient RNA, doublets, and sequencing depth can affect results.

## Boundaries
UMAP distances are not calibrated biological distances. A marker gene alone does not prove cell identity, function, or disease relevance. One healthy-donor PBMC dataset cannot support broad population conclusions. This workflow is not for clinical diagnosis.

Record dataset provenance, parameters, filtering decisions, software versions, and random seeds.


## Working labels in this project

The exported `cluster_annotations.csv` is a starting point for review, not a cell-type ground truth. Labels were assigned from a short list of observed marker patterns and should be checked against the dot plot and a suitable PBMC reference before being used in a report.

- A cluster with `CD3D/CD3E` expression is T-cell-enriched; additional markers are needed to separate naive, memory, CD4, and CD8 populations.
- `LYZ`, `S100A8/S100A9`, and `FCN1` support a classical-monocyte-like label.
- `NKG7`, `PRF1`, and granzymes indicate cytotoxic lymphocytes, but do not alone distinguish NK cells from cytotoxic T cells.
- `MS4A1`, `CD79A`, and `CD79B` support a B-cell-like label.
- `FCGR3A` with `LST1/FCER1G` supports a non-classical-monocyte-like interpretation, which still needs checking against the full marker profile.
- `FCER1A/CLEC10A` may indicate dendritic/APC-like cells; this cluster is small and needs extra caution.
- `PPBP/PF4` supports a platelet-associated population.
- Small clusters with weak or ribosomal-dominated signatures should remain unresolved until stronger evidence is available.

The marker dot plot encodes scaled mean expression by colour and the fraction of cells expressing each marker by dot size. It is a visual check, not a statistical test. Differential-expression p-values from cell-level comparisons can be overly optimistic because cells from the same donor are not independent biological replicates. Treat this single-donor analysis as exploratory.
