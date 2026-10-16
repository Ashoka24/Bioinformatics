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
