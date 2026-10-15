# WES Results Directory

This directory separates the completed local HCC1395/HCC1395BL run from the planned GSE179296 / Sample 1001 public pilot.

## Completed local run

- [HCC1395 execution and validation report](hcc1395_sarek/REPORT.md)
- Final filtered, VEP-annotated VCF reported by the run: `annotation/mutect2/HCC1395_vs_HCC1395BL/HCC1395_vs_HCC1395BL.mutect2.filtered_VEP.ann.vcf.gz`
- MultiQC report reported by the run: `multiqc/multiqc_report.html`

The report records 5,289 VCF records, a VEP `CSQ` header, passing gzip integrity validation, and a present Tabix index. The index query was not independently validated in the recorded checks. These are workflow-level checks, not clinical interpretation.

## Recommended publication policy

Include only selected, reviewable deliverables:

1. FastQC HTML reports for the analyzed samples, when present.
2. MultiQC HTML report and a concise QC summary.
3. The final filtered, VEP-annotated VCF and its index, if file sizes and data-sharing permissions allow.
4. Small summary tables and reproducible comparison metrics, if they were generated from actual outputs.
5. A run manifest recording file paths, sizes, checksums, software versions, and validation status.

Do not commit raw FASTQ/SRA reads, BAM/CRAM files, large intermediate outputs, reference assets, Nextflow `work/` files, credentials, or machine-specific absolute paths. Keep the original P1001 samplesheet unchanged; store other sample configurations as separate example files.

## Interpretation boundary

A VCF record count is not a count of pathogenic variants. This project is for computational portfolio demonstration, not clinical diagnosis. Distinguish results actually produced by a run from planned steps and from biological interpretation.
