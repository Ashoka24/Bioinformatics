# Project 07 — WES Variant Analysis

A reproducible matched tumor/normal whole-exome sequencing workflow using a real public NCBI dataset. The project is built around **Illumina WES + nf-core/sarek**, not Nanopore; Nanopore will be used in a separate long-read project.

## Dataset

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

**Omics:** WES, matched tumor/normal somatic analysis  
**Workflow:** Nextflow, nf-core/sarek, Docker  
**Programming:** Python, Bash  
**NGS:** FastQC, Fastp, BWA-MEM2, SAMtools, GATK/Mutect2, VEP  
**Cloud:** AWS S3, EC2, IAM-aware execution  
**Versioning:** Git/GitHub

## Results status

The repository currently contains the reproducible workflow and reporting structure. No biological variant counts are claimed until the public FASTQ pair has actually been processed through the workflow. This prevents placeholder metrics from being presented as experimental results.

## Interpretation boundary

This is a research/portfolio workflow. Variant calls are not clinical diagnoses, and clinical interpretation would require validated pipelines, appropriate controls, annotation and laboratory/clinical review.