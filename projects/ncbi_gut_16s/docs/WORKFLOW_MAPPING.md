# Supplied IOM Workflow vs Enhanced NCBI Workflow

## Stage 1 — VM connection

The supplied workflow starts with VM access and protected SSH credentials.

Enhanced version:

- no private key is stored in Git;
- existing VM/storage conventions are retained;
- authentication stays outside Git.

## Stage 2 — Data collection

Supplied workflow:

- vendor FASTQ download.

Enhanced version:

- NCBI SRA accession is recorded;
- `prefetch` downloads the SRA object;
- `fasterq-dump` creates paired FASTQ;
- `pigz` compresses reads;
- SHA256 checksums are stored.

## Stage 3 — QC

Supplied workflow:

- FastQC;
- MultiQC;
- review quality to determine trimming.

Enhanced version:

- same FastQC/MultiQC stage;
- read-count validation;
- paired-end consistency check;
- checksum verification;
- primer/amplicon compatibility check.

## Stage 4 — File renaming

The vendor workflow uses an ID mapping script because vendor IDs and internal IDs differ.

For NCBI data, the accession itself is the reproducible sample identifier, so a vendor ID-mapping script is not required.

## Stage 5 — Storage

The supplied workflow uses nftower storage.

Enhanced version:

`/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S/`

with separate RawData, QC, Analysis, Downstream, Results, Metadata, Params, Logs and work_dir directories.

## Stage 6 — Ampliseq

The supplied workflow uses nf-core/ampliseq 2.11.0, Docker, parameter JSON, 341F/806R primers, 280/260 truncation, SILVA taxonomy and resource limits.

Those values are retained as the baseline experiment.

The enhanced workflow adds:

- version logging;
- accession provenance;
- reproducible input preparation;
- Nextflow log capture;
- result inventory;
- post-pipeline QC;
- downstream ecological analysis.

## Stage 7 — Biological interpretation

The enhanced workflow explicitly separates:

1. technical QC;
2. ASV/taxonomy generation;
3. alpha diversity;
4. beta diversity;
5. abundance visualization;
6. statistical testing;
7. biological interpretation;
8. limitations.

This prevents a polished abundance plot from being mistaken for biological evidence.
