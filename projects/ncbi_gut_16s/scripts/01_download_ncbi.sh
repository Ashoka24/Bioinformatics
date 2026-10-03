#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"
ACCESSION="SRR26534086"

mkdir -p "$PROJECT/RawData/$ACCESSION"/{sra,fastq,checksums}

prefetch "$ACCESSION" \
  --output-directory "$PROJECT/RawData/$ACCESSION/sra" \
  --max-size 10G

SRA="$PROJECT/RawData/$ACCESSION/sra/$ACCESSION/$ACCESSION.sra"
test -s "$SRA"

fasterq-dump "$SRA" \
  --split-files \
  --threads 4 \
  --outdir "$PROJECT/RawData/$ACCESSION/fastq"

pigz -p 4 "$PROJECT/RawData/$ACCESSION/fastq/"*.fastq

sha256sum "$PROJECT/RawData/$ACCESSION/fastq/"*.fastq.gz \
  > "$PROJECT/RawData/$ACCESSION/checksums/sha256sums.txt"

echo "NCBI download and FASTQ extraction complete: $ACCESSION"
