# Project 07 — WES Variant Analysis

Whole-exome sequencing workflow for germline SNV and indel discovery.

## Objective

Build a reproducible WES analysis workflow from paired-end FASTQ files to a filtered variant table suitable for downstream review.

The project uses GitHub for code, Docker for the software environment, Nextflow for workflow orchestration, and S3 for large input/output files.

## Workflow

FASTQ → FastQC / MultiQC → Fastp → BWA-MEM2 → SAMtools → duplicate marking → GATK processing → germline variant calling → filtering → annotation → VCF + summary

## Skills demonstrated

- WES data handling
- Linux and Bash scripting
- Python result summarization
- GATK / SAMtools concepts
- Nextflow workflow orchestration
- Dockerized execution
- Git/GitHub version control
- AWS S3-compatible input/output

## Cloud execution

For AWS execution, FASTQ, reference files and generated results live in S3 while compute runs on EC2 or a compatible HPC environment.

See [AWS portfolio architecture](../../docs/AWS_OMICS_ARCHITECTURE.md).

## Repository structure

```text
07_wes_variant_analysis/
├── README.md
├── metadata/
├── config/
├── workflow/
├── scripts/
├── docker/
├── results/
└── figures/
```

## Reproducibility

No patient data is stored in the repository. Public or approved test data should be staged outside Git and referenced through the sample sheet.

## Interpretation boundary

This demonstrates variant-processing methodology. It is not a clinical diagnostic pipeline.
