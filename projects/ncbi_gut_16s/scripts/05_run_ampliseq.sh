#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"

nextflow run nf-core/ampliseq \
  -r 2.11.0 \
  -name NCBI_Gut_SRR26534086 \
  -work-dir "$PROJECT/work_dir/ampliseq" \
  -params-file "$PROJECT/Params/ampliseq_params.json" \
  -profile docker \
  -resume \
  2>&1 | tee "$PROJECT/Logs/ampliseq.log"

echo "Ampliseq finished. Inspect the log before biological interpretation."
