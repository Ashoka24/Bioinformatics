#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"
ACCESSION="SRR26534086"

FASTQ="$PROJECT/RawData/$ACCESSION/fastq"
FASTQC="$PROJECT/QC/fastqc_raw"
MULTIQC="$PROJECT/QC/multiqc_raw"

mkdir -p "$FASTQC" "$MULTIQC"

fastqc "$FASTQ/"*.fastq.gz \
  --outdir "$FASTQC" \
  --threads 4

multiqc "$FASTQC" \
  --outdir "$MULTIQC" \
  --filename multiqc_raw.html

echo "QC complete."
