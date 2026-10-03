#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"
ACCESSION_FILE="$PROJECT/Metadata/cohort_accessions.txt"

mkdir -p "$PROJECT/RawData/cohort"

while IFS= read -r ACCESSION; do
  [[ -z "$ACCESSION" ]] && continue
  [[ "$ACCESSION" =~ ^# ]] && continue

  echo "=== Downloading $ACCESSION ==="

  mkdir -p "$PROJECT/RawData/cohort/$ACCESSION"/{sra,fastq,checksums,input}

  prefetch "$ACCESSION" \
    --output-directory "$PROJECT/RawData/cohort/$ACCESSION/sra" \
    --max-size 10G

  SRA="$PROJECT/RawData/cohort/$ACCESSION/sra/$ACCESSION/$ACCESSION.sra"

  fasterq-dump "$SRA" \
    --split-files \
    --threads 4 \
    --outdir "$PROJECT/RawData/cohort/$ACCESSION/fastq"

  pigz -p 4 "$PROJECT/RawData/cohort/$ACCESSION/fastq/"*.fastq

  sha256sum "$PROJECT/RawData/cohort/$ACCESSION/fastq/"*.fastq.gz \
    > "$PROJECT/RawData/cohort/$ACCESSION/checksums/sha256sums.txt"

done < "$ACCESSION_FILE"

echo "Cohort download complete."
