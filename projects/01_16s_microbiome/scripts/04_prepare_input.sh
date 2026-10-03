#!/usr/bin/env bash
set -euo pipefail
DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
FASTQ_DIR="$PROJECT_DIR/RawData/SRR26534086/fastq"
INPUT_DIR="$PROJECT_DIR/RawData/SRR26534086/input"
mkdir -p "$INPUT_DIR"
ln -sfn "$FASTQ_DIR/SRR26534086_1.fastq.gz" "$INPUT_DIR/SRR26534086_1.fastq.gz"
ln -sfn "$FASTQ_DIR/SRR26534086_2.fastq.gz" "$INPUT_DIR/SRR26534086_2.fastq.gz"
ls -lh "$INPUT_DIR"
