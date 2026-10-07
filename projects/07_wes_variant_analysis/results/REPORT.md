# Project 07 — WES Analysis Report

## Dataset

GSE179296 / SRP326537, public NCBI WES dataset.

Pilot pair:

- Sample 1001 Normal — GSM5413848
- Sample 1001 Tumor — GSM5413849

NCBI reports 2 × 100 bp paired-end sequencing with SureSelect Human All Exon V5 capture and hg38 processing. citeturn2search0turn2search4

## Analysis status

The repository contains the reproducible workflow definition and public dataset selection. Large FASTQ, BAM and VCF files are intentionally not committed to GitHub.

Biological result metrics will be populated from the actual AWS/Nextflow run rather than invented.

## Expected outputs

- raw-read QC
- trimmed-read QC
- alignment statistics
- duplicate metrics
- BQSR metrics
- tumor/normal somatic VCF
- filtered PASS variants
- functional annotation
- MultiQC summary

## Interpretation boundary

Results are intended for portfolio demonstration and method development. They are not clinical diagnostic results.
