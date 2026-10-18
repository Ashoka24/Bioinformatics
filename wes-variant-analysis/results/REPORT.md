# Project 07 — WES Analysis Report

This repository contains a completed local nf-core/sarek 3.10.0 run for the matched HCC1395 tumor/normal pair. The detailed execution record is in [the run report](hcc1395_sarek/REPORT.md).

## Analyzed pair

- Tumor: HCC1395
- Normal: HCC1395BL
- Reference: GATK GRCh38
- Variant caller: Mutect2
- Annotation: Ensembl VEP
- Reported VCF records: 5,289
- VCF gzip integrity: passed
- VEP CSQ header: present
- Tabix index: present; indexed queries were not independently tested

The separate GSE179296 / Sample 1001 public pilot is not the dataset represented by this completed HCC1395 report.

## Interpretation

These are workflow-validation outputs, not clinical conclusions. A VCF record count is not a count of pathogenic or clinically significant variants. Interpretation requires review of filtering, annotation, sample provenance, and quality metrics.
