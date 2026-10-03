#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"
ACCESSION="SRR26534086"
FASTQ="$PROJECT/RawData/$ACCESSION/fastq"

for f in "$FASTQ/"*.fastq.gz; do
  echo "FILE: $f"
  zcat "$f" | awk 'END {print "READS:", NR/4}'
done

R1=$(zcat "$FASTQ/$ACCESSION_1.fastq.gz" | awk 'END{print NR/4}')
R2=$(zcat "$FASTQ/$ACCESSION_2.fastq.gz" | awk 'END{print NR/4}')

echo "R1=$R1"
echo "R2=$R2"

if [[ "$R1" -ne "$R2" ]]; then
  echo "ERROR: paired read counts differ"
  exit 1
fi

sha256sum -c "$PROJECT/RawData/$ACCESSION/checksums/sha256sums.txt"

echo "FASTQ validation: PASS"
