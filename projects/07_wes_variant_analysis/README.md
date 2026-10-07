# Project 07 — WES Variant Analysis

A reproducible tumor/normal whole-exome sequencing workflow using a public NCBI dataset.

## Dataset

**NCBI GEO:** GSE179296  
**SRA study:** SRP326537  
**BioProject:** PRJNA743078  
**Pilot pair:** Sample 1001 normal + Sample 1001 tumor  
**Platform:** Illumina HiSeq 2500  
**Capture:** Agilent SureSelect Human All Exon V5 (51 Mb)  
**Reads:** 2 × 100 bp paired-end  
**Reference:** hg38 / GRCh38

NCBI describes this study as WES of cutaneous squamous cell carcinoma and reports a BWA-MEM → duplicate marking → base recalibration → Mutect2 → FilterMutectCalls workflow. citeturn2search0turn2search4

## Objective

Take one public matched tumor/normal WES pair from NCBI and reproduce the main computational path:

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
Tumor/normal Mutect2
   ↓
FilterMutectCalls
   ↓
Variant annotation
   ↓
VCF + QC report
```

The production workflow uses **nf-core/sarek 3.10.0**, which supports WES, tumor/normal pairs, preprocessing, variant calling and annotation. citeturn8search0turn8search7

## Why this dataset

GSE179296 contains 33 matched normal/tumor pairs, giving the portfolio a real paired WES use case rather than a synthetic FASTQ example. citeturn2search0

## Execution

### Resolve the SRA runs

```bash
pip install pysradb
mkdir -p work
pysradb metadata --detailed SRP326537 > work/sra_metadata.tsv
```

Use **GSM5413848** and **GSM5413849** to identify the corresponding run accessions.

### Download the selected pair

```bash
export NORMAL_SRR=<normal-run-accession>
export TUMOR_SRR=<tumor-run-accession>
bash scripts/download_sra_samples.sh
```

### Run nf-core/sarek

```bash
nextflow run nf-core/sarek -r 3.10.0 \
  -profile docker \
  --input config/samplesheet.csv \
  --outdir results \
  --genome GATK.GRCh38 \
  --wes \
  --tools mutect2,vep
```

Sarek recommends pinning a release for reproducibility and supports Docker-based execution and tumor/normal pairing through the sample sheet. citeturn8search3turn8search5

## AWS execution

```text
NCBI SRA
   ↓
S3 raw/
   ↓
EC2 + Docker + Nextflow
   ↓
nf-core/sarek
   ↓
S3 results/
```

Large FASTQ, reference and result files stay in S3. GitHub contains the workflow, metadata, scripts and documentation.

## Skills demonstrated

**Omics:** WES, tumor/normal somatic variant analysis  
**Workflow:** Nextflow, nf-core/sarek, Docker  
**Programming:** Bash, Python  
**NGS tools:** FastQC, Fastp, BWA-MEM2, SAMtools, GATK/Mutect2, VEP  
**Cloud:** AWS S3, EC2, IAM-aware execution  
**Versioning:** Git/GitHub

## Interpretation boundary

The workflow is a research portfolio implementation. Variant calls are not clinical diagnoses, and no pathogenicity claim is made without appropriate clinical annotation and validation.
