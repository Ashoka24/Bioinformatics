#!/usr/bin/env bash
set -euo pipefail

# Project 07 AWS runner for the actual HCC1395/HCC1395BL matched pair.
# S3 input prefix must contain the four expected FASTQ files.
# Credentials must come from the EC2 instance IAM role.

S3_INPUT="${1:?Usage: $0 <s3-input-prefix> <s3-output-prefix>}"
S3_OUTPUT="${2:?Missing S3 output prefix}"
PROJECT_DIR="${PROJECT_DIR:-/workspace/Bioinformatics/projects/07_wes_variant_analysis}"
FASTQ_DIR="$PROJECT_DIR/work/fastq/hcc1395"

mkdir -p "$FASTQ_DIR" "$PROJECT_DIR/results"
aws s3 sync "$S3_INPUT" "$FASTQ_DIR" --only-show-errors

cd "$PROJECT_DIR"
for file in \
  HCC1395_N_R1.recovered.fastq.gz \
  HCC1395_N_R2.recovered.fastq.gz \
  HCC1395_T_R1.fastq.gz \
  HCC1395_T_R2.fastq.gz
do
  [[ -s "$FASTQ_DIR/$file" ]] || { echo "Missing input FASTQ: $FASTQ_DIR/$file" >&2; exit 1; }
done

bash scripts/run_sarek.sh
aws s3 sync "$PROJECT_DIR/results" "$S3_OUTPUT" --only-show-errors

echo "Project 07 HCC1395/HCC1395BL results synced to $S3_OUTPUT"
