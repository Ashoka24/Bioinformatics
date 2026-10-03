#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"

mkdir -p "$PROJECT/Results"

find "$PROJECT/Analysis/ampliseq" -type f \
  > "$PROJECT/Results/ampliseq_file_inventory.txt"

find "$PROJECT/Analysis/ampliseq" \
  \( -name "*.qza" -o -name "*.qzv" -o -name "*.tsv" \) \
  -print \
  > "$PROJECT/Results/qiime_artifact_inventory.txt"

echo "Result inventory written."
