#!/usr/bin/env bash
set -euo pipefail

PIPELINE_VERSION="3.27.0"

echo "Project 04: nf-core/rnaseq ${PIPELINE_VERSION}"
echo "Nextflow version:"
nextflow -version

echo "Launching reproducible Docker test..."
nextflow run nf-core/rnaseq \
  -r "${PIPELINE_VERSION}" \
  -profile test,docker \
  -name project04_nfcore_test
