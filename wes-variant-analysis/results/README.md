# WES Results Directory

## Completed local HCC1395/HCC1395BL run

- **Tumor sample:** `HCC1395` (`status=1`)
- **Normal sample:** `HCC1395BL` (`status=0`)
- **Patient ID:** `HCC1395`
- **Output pair label:** `HCC1395_vs_HCC1395BL`
- [Execution and validation report](hcc1395_sarek/REPORT.md)
- Final filtered VEP-annotated VCF reported by the run: `annotation/mutect2/HCC1395_vs_HCC1395BL/HCC1395_vs_HCC1395BL.mutect2.filtered_VEP.ann.vcf.gz`
- MultiQC report reported by the run: `multiqc/multiqc_report.html`

The report records 5,289 VCF records, a VEP `CSQ` header, passing gzip integrity validation, and a present Tabix index. Index-query validation was not independently completed in the recorded checks.

## Samplesheet validation

The root samplesheet, `../config/samplesheet.csv`, is configured for this pair. Validate its structure and pairing with:

```bash
python3 scripts/validate_samplesheet.py
```

From the project root, validate actual input file existence and gzip integrity with:

```bash
python3 scripts/validate_samplesheet.py --check-files
```

Raw FASTQ/SRA reads, BAM/CRAM files, reference assets, Nextflow work files, and credentials should remain outside GitHub. Publish only reviewed, appropriately sized outputs and summaries.

## Interpretation boundary

A VCF record count is not a count of pathogenic variants. This project demonstrates a computational workflow and is not a clinical diagnostic pipeline.
