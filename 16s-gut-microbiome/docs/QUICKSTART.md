# Quickstart — Project 01

This guide runs the public NCBI 16S workflow from a WSL terminal. It is intentionally written as an execution checklist so the repository can be followed from a clean environment.

## 1. Clone and enter the repository

```bash
git clone https://github.com/Ashoka24/Bioinformatics.git
cd Bioinformatics/projects/01_16s_microbiome
```

## 2. Check the environment

```bash
bash scripts/00_setup.sh
```

The setup check reports CPU, memory, disk space and the required command-line tools. Do not start the pipeline if a required tool is missing.

## 3. Download the public run

The default run is `SRR26534086`.

```bash
bash scripts/01_download_ncbi.sh
```

The script:

1. downloads the SRA record with NCBI SRA Toolkit;
2. validates the SRA file with `vdb-validate`;
3. converts it to paired FASTQ;
4. compresses the FASTQ files;
5. writes SHA-256 checksums.

Raw files are written outside Git under:

```text
/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data/16s_ncbi_gut/
```

To use another local data root:

```bash
DATA_ROOT=/path/to/data bash scripts/01_download_ncbi.sh
```

## 4. Run read-level QC

```bash
bash scripts/02_qc.sh
```

Inspect the generated MultiQC report before changing trimming or truncation parameters.

## 5. Validate paired reads

```bash
bash scripts/03_validate.sh
```

This verifies checksums and confirms that R1 and R2 contain the same number of reads.

## 6. Prepare the nf-core/ampliseq input

```bash
bash scripts/04_prepare_input.sh
```

The input directory contains symlinks to the validated FASTQ files, so the raw files are not duplicated.

## 7. Run nf-core/ampliseq

```bash
bash scripts/05_run_ampliseq.sh
```

The repository tracks the intended analysis parameters in `params/ampliseq_params.json`. The execution script creates a runtime copy with the local data path rewritten automatically.

The workflow uses:

- nf-core/ampliseq 2.11.0
- Docker profile
- paired-end V3–V4 16S primers
- forward truncation: 280
- reverse truncation: 260
- SILVA taxonomy
- DADA2/QIIME 2 processing

The actual pipeline output remains outside Git.

## 8. Run downstream analysis

After a successful pipeline run:

```bash
bash scripts/05_qiime2_downstream.sh
```

The script discovers the feature table and taxonomy artifacts when possible and performs descriptive downstream analysis.

## 9. Expand from one run to the parent BioProject

```bash
bash scripts/06_expand_bioproject.sh
```

This retrieves run metadata for `PRJNA1031545`. Cohort-level analysis should only be added after the metadata are inspected and the biological groups are explicitly defined.

## Reproducibility rule

Do not copy generated reports, FASTQ files, QIIME 2 artifacts, Nextflow work directories or private/company data into the repository. Commit scripts, parameters, metadata definitions, documentation and genuine observations instead.
