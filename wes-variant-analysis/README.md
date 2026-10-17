# Whole-Exome Sequencing Variant Analysis with nf-core/sarek

A matched tumor/normal whole-exome sequencing workflow using **Illumina WES and nf-core/sarek 3.10.0**. The primary samplesheet uses the actual pair analyzed for this project: **HCC1395 tumor** and **HCC1395BL normal**.

## MultiQC report evidence

The repository contains the MultiQC HTML report generated for the HCC1395 tumor/normal Sarek run. Open the [MultiQC report](results/hcc1395_sarek/multiqc/multiqc_report.html) to inspect the report sections directly. This links to the generated report rather than using a recreated screenshot.

## Primary sample pair

| Patient | Sample ID | Role | Sarek status |
|---|---|---|---|
| HCC1395 | HCC1395BL | Normal | `0` |
| HCC1395 | HCC1395 | Tumor | `1` |

The primary input is [`config/samplesheet.csv`](config/samplesheet.csv). Both rows share the same `patient` identifier, as required for matched tumor/normal analysis. The paired FASTQ files are expected locally under `work/fastq/hcc1395/`; raw reads are not committed to GitHub.

The completed local run is documented in [`results/hcc1395_sarek/REPORT.md`](results/hcc1395_sarek/REPORT.md). The report records 5,289 VCF records, a VEP `CSQ` header, a passing gzip integrity check, and a present Tabix index. The index was not independently query-tested in the recorded checks.

## Workflow

```text
Paired FASTQ files
   ↓
FastQC / MultiQC and preprocessing
   ↓
BWA-MEM2 alignment
   ↓
BAM processing and duplicate marking
   ↓
Mutect2 tumor/normal calling
   ↓
FilterMutectCalls
   ↓
VEP annotation
   ↓
Filtered annotated VCF + QC report
```

Execution is delegated to nf-core/sarek 3.10.0.

## Project structure

```text
07_wes_variant_analysis/
├── config/
│   ├── samplesheet.csv
│   └── samplesheet.hcc1395.example.csv
├── metadata/DATASET.md
├── scripts/
│   ├── validate_samplesheet.py
│   ├── run_sarek.sh
│   ├── summarize_variants.py
│   └── prepare_curated_results.sh
├── results/hcc1395_sarek/REPORT.md
└── figures/workflow.svg
```

## Validate the samplesheet and input FASTQs

Run these commands from this project directory:

```bash
# Check required columns, sample IDs, matched-pair status and duplicate rows
python3 scripts/validate_samplesheet.py

# Also require all four FASTQ files to exist and verify gzip integrity
python3 scripts/validate_samplesheet.py --check-files
```

The first command validates the samplesheet metadata and tumor/normal pairing. The second additionally reads each compressed FASTQ to EOF, checking that the files exist and are not truncated/corrupt. FASTQ validation must be run on the machine where the local files are present; GitHub does not contain the raw reads.

## Run nf-core/sarek

First confirm Docker and Nextflow are installed and running, then:

```bash
bash scripts/run_sarek.sh
```

The wrapper validates the samplesheet and FASTQ files before starting Sarek. Defaults are:

- Sarek: `3.10.0`
- Reference profile: `GATK.GRCh38`
- Mode: WES
- Tools: `mutect2,vep`
- Input: `config/samplesheet.csv`
- Output directory: `results`

Optional environment variables: `INPUT`, `OUTDIR`, `SAREK_VERSION`, and `GENOME`.

## Curated results and repository hygiene

Use `scripts/prepare_curated_results.sh` after a successful run to stage only selected reports, small result tables, the final filtered annotated VCF/index (subject to size limits), and a manifest. Review staged files before committing. Do not commit raw FASTQ/SRA reads, BAM/CRAM files, reference assets, Nextflow work directories, Docker storage, credentials, or machine-specific absolute paths.

## Completion and interpretation boundary

**Core workflow status: completed locally for HCC1395/HCC1395BL.** The validation details and limitations are recorded in the execution report. These are workflow-level checks, not clinical conclusions; a VCF record count is not a count of pathogenic variants. Clinical interpretation requires appropriate validation and expert review.
