# Project 07 — WES Variant Analysis

A reproducible matched tumor/normal whole-exome sequencing workflow using a real public NCBI dataset. The project is built around **Illumina WES + nf-core/sarek**, not Nanopore; Nanopore will be used in a separate long-read project.

## Sample identity and run status

This project documents **two distinct matched tumor/normal pairs**. Their identifiers must not be mixed:

| Run | Normal sample ID | Tumor sample ID | Status | Which outputs belong to it? |
|---|---|---|---|---|
| **Core deliverable — completed** | `HCC1395BL` (`status=0`) | `HCC1395` (`status=1`) | **Completed and validated locally** | `results/hcc1395_sarek/`; VCF pair label `HCC1395_vs_HCC1395BL` |
| Optional public extension, Sample 1001 | `N1001` / GEO `GSM5413848` | `T1001` / GEO `GSM5413849` | Documented extension; not executed/verified as part of the completed deliverable | `config/samplesheet.csv` is the public-pilot samplesheet; it is not the source of the published HCC1395 VCF |

The curated VCF currently published in this repository is from the **HCC1395/HCC1395BL local run**, not Sample 1001. The local example samplesheet is [`config/samplesheet.hcc1395.example.csv`](config/samplesheet.hcc1395.example.csv); the public-pilot samplesheet remains [`config/samplesheet.csv`](config/samplesheet.csv).

## Public pilot dataset (Sample 1001)

**NCBI GEO:** GSE179296  
**SRA study:** SRP326537  
**BioProject:** PRJNA743078  
**Pilot pair:** GSM5413848 (normal) + GSM5413849 (tumor), Sample 1001  
**Platform:** Illumina HiSeq 2500  
**Capture:** Agilent SureSelect Human All Exon V5 (51 Mb)  
**Reads:** 2 × 100 bp paired-end  
**Reference:** hg38 / GRCh38

The study contains 33 matched normal/tumor pairs. The NCBI submission describes a WES workflow using alignment, duplicate marking, base recalibration, Mutect2 and filtering. citeturn2search0turn2search4

## Objective

Process one real public matched WES pair from SRA through QC, alignment, preprocessing, somatic variant calling and annotation:

```text
NCBI SRA
   ↓
FASTQ
   ↓
FastQC / MultiQC
   ↓
Fastp
   ↓
BWA-MEM2
   ↓
BAM sorting + duplicate marking
   ↓
Base-quality recalibration
   ↓
Mutect2 tumor/normal
   ↓
FilterMutectCalls
   ↓
VEP annotation
   ↓
VCF + QC report
```

The production workflow delegates execution to **nf-core/sarek 3.10.0**, which supports WES, tumor/normal pairing, mapping, BAM processing, Mutect2, VEP and MultiQC. citeturn0search2turn0search9

## Project structure

```text
07_wes_variant_analysis/
├── config/samplesheet.csv
├── metadata/DATASET.md
├── workflow/main.nf
├── scripts/
│   ├── resolve_sra_runs.py
│   ├── download_sra_samples.sh
│   ├── run_sarek.sh
│   └── summarize_variants.py
├── docker/Dockerfile
├── results/REPORT.md
└── figures/workflow.svg
```

## Execution

### 1. Resolve the NCBI/SRA runs

```bash
pip install pysradb
python scripts/resolve_sra_runs.py
cat work/selected_sra_runs.tsv
```

The resolver maps the two GEO samples to their SRA run accessions so the repository does not hard-code an unverified run ID.

### 2. Download the paired FASTQ files

```bash
bash scripts/download_sra_samples.sh
ls -lh work/fastq/
```

The downloader reads `work/selected_sra_runs.tsv`, retrieves both runs with SRA Toolkit and writes the expected files:

```text
work/fastq/N1001_R1.fastq.gz
work/fastq/N1001_R2.fastq.gz
work/fastq/T1001_R1.fastq.gz
work/fastq/T1001_R2.fastq.gz
```

Raw FASTQ files are intentionally not committed to GitHub.

### 3. Run nf-core/sarek

```bash
nextflow run nf-core/sarek -r 3.10.0 -profile docker \\
  --input config/samplesheet.csv \\
  --outdir results \\
  --genome GATK.GRCh38 \\
  --wes \\
  --tools mutect2,vep \\
  -resume
```

Or use the project wrapper:

```bash
bash scripts/run_sarek.sh
```

The samplesheet uses the same `patient` ID for normal and tumor and `status=0/1`, which is the Sarek convention for tumor/normal pairing. citeturn0search0turn0search1

### 4. Test the environment before the real run

For a new Nextflow/Sarek installation, run the upstream test profile before starting the large public dataset. The Sarek documentation explicitly recommends testing the setup before running actual data. citeturn0search8

```bash
nextflow run nf-core/sarek -r 3.10.0 -profile test,docker
```

## Curate and publish completed results

After the local Sarek run has completed, prepare a small, reviewable set of outputs for GitHub:

```bash
bash scripts/prepare_curated_results.sh
git diff --cached --check
git diff --cached --name-only
git diff --cached --stat
```

The helper stages only selected FastQC HTML, MultiQC HTML, small CSV/TSV result tables, the final filtered VEP-annotated VCF and its index (when present and within the configured size thresholds), plus a manifest and summary. It deliberately does not commit or push automatically. Review the staged files before committing. Do not stage the entire `results/` tree or raw/intermediate sequencing files.

## AWS execution

```text
NCBI SRA
   ↓
S3 raw/
   ↓
EC2 compute + IAM role
   ↓
Docker + Nextflow
   ↓
nf-core/sarek 3.10.0
   ↓
S3 results/
   ↓
GitHub report / QC summary
```

Large sequencing, reference and workflow-result files stay outside GitHub. AWS credentials are not stored in the repository.

## Skills demonstrated

**Omics and variant analysis:** Whole-exome sequencing (WES), matched tumor/normal design, somatic variant calling, variant filtering, VEP annotation, VCF validation  
**Workflow and containers:** Nextflow, nf-core/sarek 3.10.0, Docker, workflow resumption with `-resume`  
**Quality control:** FastQC, MultiQC, Fastp, gzip integrity validation, VCF/header checks  
**NGS tools:** BWA-MEM2, SAMtools, GATK/Mutect2, FilterMutectCalls, Ensembl VEP  
**Programming and automation:** Python, Bash, JSON configuration, Git/GitHub, GitHub Actions  
**Cloud concepts:** AWS S3, EC2, IAM-aware execution design

### Tools used

- **Workflow:** Nextflow, nf-core/sarek 3.10.0
- **Execution:** Docker
- **Read QC/preprocessing:** FastQC, MultiQC, Fastp
- **Alignment and BAM processing:** BWA-MEM2, SAMtools, GATK preprocessing tools
- **Somatic variant calling/filtering:** GATK Mutect2, FilterMutectCalls
- **Annotation:** Ensembl Variant Effect Predictor (VEP)
- **Validation and reporting:** gzip integrity check, VCF record/header checks, MultiQC HTML
- **Code and delivery:** Python, Bash, Git, GitHub, GitHub Actions
- **Cloud-ready components:** AWS S3, EC2, IAM

Cloud services are documented as the intended execution pattern; the completed HCC1395 run described below was local, not an AWS deployment.

## Results status — core project completed

**Completion status: COMPLETE for the local HCC1395/HCC1395BL matched tumor/normal workflow.** The execution report is in [`results/hcc1395_sarek/REPORT.md`](results/hcc1395_sarek/REPORT.md). Recorded validation includes 5,289 VCF records, a present VEP `CSQ` header, a passing gzip integrity check, and a present Tabix index. The index file was not independently query-tested in the recorded checks.

The separate GSE179296 / Sample 1001 (`N1001` / `T1001`) public pilot remains a documented optional extension and is not included in the completed status. The repository does not claim that the HCC1395 results came from Sample 1001 or that AWS was used for the local run.

Raw sequencing files, reference assets, Nextflow work files, and Docker storage are intentionally kept out of GitHub. Only reproducible code, reusable configuration, documentation, and selected lightweight reports should be version-controlled.

## Interpretation boundary

This is a research/portfolio workflow. Variant calls are not clinical diagnoses, and clinical interpretation would require validated pipelines, appropriate controls, annotation and laboratory/clinical review.