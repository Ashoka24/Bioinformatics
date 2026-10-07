# Dataset — Project 07 WES

## Public NCBI dataset

**NCBI GEO:** GSE179296 — *COL11A1 mutations in cutaneous squamous cell carcinoma [WES]*  
**NCBI SRA study:** SRP326537  
**BioProject:** PRJNA743078  
**Platform:** Illumina HiSeq 2500  
**Capture:** Agilent SureSelect Human All Exon V5 (51 Mb)  
**Reads:** 2 × 100 bp paired-end  
**Reference reported by the study:** hg38 / GRCh38

NCBI reports 66 samples in the series, arranged as matched normal skin and cSCC tumor samples for 33 sample IDs. The study describes BWA-MEM alignment, duplicate marking, base recalibration, Mutect2 somatic calling and FilterMutectCalls filtering. citeturn2search0turn1view0

## Portfolio pilot pair

| Patient | Role | GEO |
|---|---|---|
| 1001 | Normal | GSM5413848 |
| 1001 | Tumor | GSM5413849 |

The tumor sample is explicitly identified by NCBI as **Sample 1001 Tumor**, using the same 51 Mb SureSelect capture and 2 × 100 bp sequencing design. citeturn2search4

The corresponding SRA run accessions are resolved at runtime from the NCBI study metadata rather than guessed or hard-coded.

## Download strategy

Raw reads remain in NCBI SRA and are **not committed to GitHub**. The workflow resolves the selected GEO records to run-level accessions and downloads the FASTQ files at execution time.

The AWS implementation stages the reads into S3 before compute. This keeps large sequencing files out of Git and allows the same workflow to run on EC2.

## Reference

The study reports **hg38 / GRCh38**. The portfolio records the exact GATK GRCh38 resource release used for each run. citeturn1view0

## Scope

1. SRA → FASTQ retrieval
2. read QC
3. WES alignment
4. duplicate marking
5. base-quality recalibration
6. tumor/normal somatic calling
7. variant filtering
8. functional annotation
9. QC and summary reporting

This is a research/portfolio workflow, not a clinical diagnostic pipeline.
