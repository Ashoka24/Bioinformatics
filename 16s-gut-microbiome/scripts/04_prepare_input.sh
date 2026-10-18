#!/usr/bin/env bash
set -euo pipefail

DATA_ROOT="${DATA_ROOT:-$HOME/bioinformatics-data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
ACCESSION="${ACCESSION:-SRR26534086}"
FASTQ_DIR="$PROJECT_DIR/RawData/$ACCESSION/fastq"
INPUT_DIR="$PROJECT_DIR/RawData/$ACCESSION/input"
R1="$FASTQ_DIR/${ACCESSION}_1.fastq.gz"
R2="$FASTQ_DIR/${ACCESSION}_2.fastq.gz"

[[ -f "$R1" ]] || { echo "ERROR: missing paired FASTQ file: $R1" >&2; exit 1; }
[[ -f "$R2" ]] || { echo "ERROR: missing paired FASTQ file: $R2" >&2; exit 1; }

mkdir -p "$INPUT_DIR"
ln -sfn "$R1" "$INPUT_DIR/${ACCESSION}_1.fastq.gz"
ln -sfn "$R2" "$INPUT_DIR/${ACCESSION}_2.fastq.gz"
ls -lh "$INPUT_DIR"
