# Operator Runbook

This is the human-style execution order.

## Day 1 — data and QC

    cd /home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S

    bash scripts/00_environment_check.sh
    bash scripts/01_download_ncbi.sh
    bash scripts/03_validate_fastq.sh
    bash scripts/02_qc.sh
    bash scripts/04_prepare_input.sh

Stop and inspect MultiQC before running Ampliseq.

## Day 2 — pipeline

    bash scripts/05_run_ampliseq.sh
    bash scripts/06_inventory_results.sh

If the pipeline fails:

1. read the last process name;
2. inspect the Nextflow work directory;
3. record requested vs available resources;
4. change one variable at a time;
5. resume with -resume.

## Day 3 — downstream

After locating the actual QIIME artifacts, edit scripts/07_qiime2_downstream.sh and run:

    bash scripts/07_qiime2_downstream.sh

For the first single sample, only descriptive alpha diversity is meaningful.

## Day 4+ — biological cohort

Discover the BioProject runs with Entrez Direct, review the metadata, create Metadata/cohort_accessions.txt, and then process the cohort using the same download/QC/Ampliseq path.

## What gets committed

Commit:

- scripts;
- parameter files;
- metadata templates;
- provenance;
- README;
- QC decision notes;
- analysis code;
- summarized results;
- figures.

Do not commit:

- private keys;
- credentials;
- large raw FASTQ;
- temporary Nextflow work directories;
- private clinical metadata.
