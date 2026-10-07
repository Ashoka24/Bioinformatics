#!/usr/bin/env bash
set -euo pipefail

# Project 07 AWS runner: stage FASTQ from S3, run pinned nf-core/sarek, sync results back.
# Credentials must come from the EC2 instance IAM role.

S3_INPUT="${1:?Usage: $0 <s3-input-prefix> <s3-output-prefix>}"
S3_OUTPUT="${2:?Missing S3 output prefix}"
PROJECT_DIR="${PROJECT_DIR:-/workspace/Bioinformatics/projects/07_wes_variant_analysis}"
WORK_DIR="$PROJECT_DIR/work"

mkdir -p "$WORK_DIR/fastq" "$PROJECT_DIR/results"
aws s3 sync "$S3_INPUT" "$WORK_DIR/fastq" --only-show-errors

cd "$PROJECT_DIR"
[[ -s "$WORK_DIR/fastq/N1001_R1.fastq.gz" ]] || { echo "Missing N1001_R1.fastq.gz" >&2; exit 1; }
[[ -s "$WORK_DIR/fastq/N1001_R2.fastq.gz" ]] || { echo "Missing N1001_R2.fastq.gz" >&2; exit 1; }
[[ -s "$WORK_DIR/fastq/T1001_R1.fastq.gz" ]] || { echo "Missing T1001_R1.fastq.gz" >&2; exit 1; }
[[ -s "$WORK_DIR/fastq/T1001_R2.fastq.gz" ]] || { echo "Missing T1001_R2.fastq.gz" >&2; exit 1; }

bash scripts/run_sarek.sh

aws s3 sync "$PROJECT_DIR/results" "$S3_OUTPUT" --only-show-errors

echo "Project 07 results synced to $S3_OUTPUT"
