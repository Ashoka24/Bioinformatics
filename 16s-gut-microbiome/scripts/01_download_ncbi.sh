#!/usr/bin/env bash
set -euo pipefail

# Windows:
# C:\Users\ashok\OneDrive\Desktop\Ashoka\data
#
# WSL:
# /mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data
DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
ACCESSION="${ACCESSION:-SRR26534086}"

SRA_DIR="$PROJECT_DIR/RawData/$ACCESSION/sra"
FASTQ_DIR="$PROJECT_DIR/RawData/$ACCESSION/fastq"
CHECKSUM_DIR="$PROJECT_DIR/RawData/$ACCESSION/checksums"

mkdir -p "$SRA_DIR" "$FASTQ_DIR" "$CHECKSUM_DIR" \
         "$PROJECT_DIR/QC" "$PROJECT_DIR/Analysis" "$PROJECT_DIR/Logs"

echo "Project: $PROJECT_DIR"
echo "Accession: $ACCESSION"

prefetch "$ACCESSION" \
    --output-directory "$SRA_DIR" \
    --max-size 10G

SRA_FILE="$SRA_DIR/$ACCESSION/$ACCESSION.sra"

if [[ ! -f "$SRA_FILE" ]]; then
    echo "ERROR: expected SRA file not found: $SRA_FILE" >&2
    exit 1
fi

vdb-validate "$SRA_FILE"

fasterq-dump "$SRA_FILE" \
    --split-files \
    --threads 4 \
    --outdir "$FASTQ_DIR"

if command -v pigz >/dev/null 2>&1; then
    pigz -p 4 "$FASTQ_DIR"/*.fastq
else
    gzip "$FASTQ_DIR"/*.fastq
fi

sha256sum "$FASTQ_DIR"/*.fastq.gz \
    > "$CHECKSUM_DIR/sha256sums.txt"

echo
echo "Downloaded and validated:"
ls -lh "$FASTQ_DIR"
echo
echo "Checksums:"
cat "$CHECKSUM_DIR/sha256sums.txt"
