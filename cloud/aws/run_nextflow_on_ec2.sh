#!/usr/bin/env bash
set -euo pipefail

# Run a project workflow on an EC2 instance using S3 for large files.
# Credentials should come from the EC2 IAM role, never from this script.

PROJECT_PATH="${1:?Usage: $0 <project-path> <s3-input> <s3-output> }"
S3_INPUT="${2:?Missing S3 input URI}"
S3_OUTPUT="${3:?Missing S3 output URI}"

mkdir -p /workspace/input /workspace/output
aws s3 sync "$S3_INPUT" /workspace/input --only-show-errors

cd "/workspace/$PROJECT_PATH"
nextflow run workflow/main.nf \
  --input /workspace/input \
  --outdir /workspace/output

aws s3 sync /workspace/output "$S3_OUTPUT" --only-show-errors
