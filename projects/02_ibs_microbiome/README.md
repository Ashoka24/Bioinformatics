# Project 02 — IBS microbiome classification

Public-data-only cohort analysis using PRJNA637763, a human gut 16S rRNA dataset containing 85 IBS samples and 26 healthy controls. The study used V1–V2 amplicon sequencing on Illumina MiSeq and was explicitly designed for microbiome-based IBS prediction.

## Objectives
1. Build a reproducible 16S feature table from public SRA/ENA FASTQ files.
2. Quantify alpha diversity and taxonomic composition.
3. Test IBS vs healthy-control community differences.
4. Build a leakage-safe microbiome classifier using genus-level abundance.
5. Report real cross-validation metrics and ranked microbial features.

## Analysis
- Public source: NCBI BioProject PRJNA637763
- Study: Usefulness of Machine Learning-Based Gut Microbiome Analysis for Identifying Patients with Irritable Bowels Syndrome
- Samples: 85 IBS + 26 healthy controls
- Region: V1–V2
- Platform: Illumina MiSeq, paired-end
- Denoising: QIIME 2 Deblur on forward reads
- Taxonomy: SILVA 138 99% classifier
- ML: scikit-learn logistic regression and random forest with stratified cross-validation

This is an independent public-data re-analysis, not a reproduction of the original paper's exact private preprocessing or model.

## Outputs
- results/REPORT.md
- results/tables/
- results/figures/
- results/ml/
- results/qc/

Raw FASTQ and intermediate QIIME artifacts are intentionally not committed.
