# Project 05 Dataset

## GSE42568 — Breast Cancer Gene Expression Analysis

Source: NCBI Gene Expression Omnibus (GEO)

Accession: GSE42568

BioProject: PRJNA182286

Platform: GPL570 — Affymetrix Human Genome U133 Plus 2.0 Array

Organism: Homo sapiens

Experiment type: Expression profiling by array

Samples:

- 104 breast cancer biopsies
- 17 normal breast tissues
- 121 total samples

The original GEO record states that the cancer biopsies were collected before treatment with tamoxifen or chemotherapy and that the study includes clinical characteristics such as ER status, tumor grade and lymph-node status.

For Project 05, the prediction target is deliberately restricted to the GEO sample-level tissue class:

- breast cancer = 1
- normal breast tissue = 0

No ER, grade, treatment or survival variable is used as a prediction target.

Data source used by the workflow:

https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE42568

The workflow downloads the processed series-matrix file at run time. Raw CEL files are not stored in this repository.
