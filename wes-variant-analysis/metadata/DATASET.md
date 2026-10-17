# Dataset and sample manifest — Project 07

## Actual analyzed pair

This project uses the matched tumor/normal pair recorded in the completed local run report.

| Patient ID | Sample ID | Role | Sarek status | Expected FASTQ prefix |
|---|---|---|---|---|
| HCC1395 | HCC1395BL | Normal | 0 | `HCC1395_N` |
| HCC1395 | HCC1395 | Tumor | 1 | `HCC1395_T` |

Expected local files:

- `work/fastq/hcc1395/HCC1395_N_R1.recovered.fastq.gz`
- `work/fastq/hcc1395/HCC1395_N_R2.recovered.fastq.gz`
- `work/fastq/hcc1395/HCC1395_T_R1.fastq.gz`
- `work/fastq/hcc1395/HCC1395_T_R2.fastq.gz`

These files are inputs on the analysis machine and are intentionally not stored in GitHub. The sample IDs, roles, and output pair label are aligned with `results/hcc1395_sarek/REPORT.md`.

## Validation

Run from the project directory:

```bash
python3 scripts/validate_samplesheet.py
python3 scripts/validate_samplesheet.py --check-files
```

The first command checks the samplesheet schema and matched tumor/normal assignments. The second also verifies that all four FASTQ files exist and that each gzip stream can be read to completion. Do not report file-level validation as passed until the second command succeeds on the machine containing the actual FASTQs.

## Scope

The workflow covers read QC, WES alignment and BAM processing, matched tumor/normal somatic calling, variant filtering, VEP annotation, and QC reporting. This is a research/portfolio workflow, not a clinical diagnostic pipeline.
