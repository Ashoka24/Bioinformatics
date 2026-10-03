#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"
ACCESSION="SRR26534086"

INPUT="$PROJECT/RawData/$ACCESSION/input"
FASTQ="$PROJECT/RawData/$ACCESSION/fastq"

mkdir -p "$INPUT"

ln -sf "$FASTQ/$ACCESSION_1.fastq.gz" "$INPUT/$ACCESSION_1.fastq.gz"
ln -sf "$FASTQ/$ACCESSION_2.fastq.gz" "$INPUT/$ACCESSION_2.fastq.gz"

ls -lah "$INPUT"

echo "Ampliseq input prepared."
