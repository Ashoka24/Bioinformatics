#!/usr/bin/env bash
set -euo pipefail
DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
FASTQ_DIR="$PROJECT_DIR/RawData/SRR26534086/fastq"
CHECKSUM_FILE="$PROJECT_DIR/RawData/SRR26534086/checksums/sha256sums.txt"
R1="$FASTQ_DIR/SRR26534086_1.fastq.gz"
R2="$FASTQ_DIR/SRR26534086_2.fastq.gz"
[[ -f "$R1" ]] || { echo "ERROR: missing $R1" >&2; exit 1; }
[[ -f "$R2" ]] || { echo "ERROR: missing $R2" >&2; exit 1; }
(cd "$FASTQ_DIR" && sha256sum -c "$CHECKSUM_FILE")
R1_READS=$(gzip -cd "$R1" | awk 'END {print NR/4}')
R2_READS=$(gzip -cd "$R2" | awk 'END {print NR/4}')
echo "R1 reads: $R1_READS"
echo "R2 reads: $R2_READS"
[[ "$R1_READS" == "$R2_READS" ]] || { echo "ERROR: paired read counts differ" >&2; exit 1; }
echo "Validation passed."
