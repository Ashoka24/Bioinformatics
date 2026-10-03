#!/usr/bin/env bash
set -euo pipefail
DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
FASTQ_DIR="$PROJECT_DIR/RawData/SRR26534086/fastq"
FASTQC_DIR="$PROJECT_DIR/QC/fastqc"
MULTIQC_DIR="$PROJECT_DIR/QC/multiqc"
mkdir -p "$FASTQC_DIR" "$MULTIQC_DIR"
shopt -s nullglob
FASTQ_FILES=("$FASTQ_DIR"/*.fastq.gz)
if [[ ${#FASTQ_FILES[@]} -eq 0 ]]; then echo "ERROR: no FASTQ files found in $FASTQ_DIR" >&2; exit 1; fi
fastqc "${FASTQ_FILES[@]}" --outdir "$FASTQC_DIR"
multiqc "$FASTQC_DIR" --outdir "$MULTIQC_DIR" --force
echo "QC complete: $MULTIQC_DIR/multiqc_report.html"
