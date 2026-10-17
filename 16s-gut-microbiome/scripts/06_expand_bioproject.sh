#!/usr/bin/env bash
set -euo pipefail
DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
BIOPROJECT="${BIOPROJECT:-PRJNA1031545}"
OUTFILE="$PROJECT_DIR/metadata/${BIOPROJECT}_runinfo.csv"
mkdir -p "$PROJECT_DIR/metadata"
command -v esearch >/dev/null || { echo "Install Entrez Direct: esearch/efetch" >&2; exit 1; }
esearch -db sra -query "$BIOPROJECT" | efetch -format runinfo > "$OUTFILE"
echo "Saved $OUTFILE"
awk 'NR > 1 {n++} END {print "Run records:", n+0}' "$OUTFILE"
head -n 10 "$OUTFILE"
