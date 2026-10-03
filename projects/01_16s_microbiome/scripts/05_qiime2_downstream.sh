#!/usr/bin/env bash
set -euo pipefail
DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
AMPLISEQ_DIR="$PROJECT_DIR/Analysis/ampliseq"
OUTDIR="$PROJECT_DIR/Analysis/qiime2_downstream"
mkdir -p "$OUTDIR"
FEATURE_TABLE_QZA="${FEATURE_TABLE_QZA:-}"
TAXONOMY_QZA="${TAXONOMY_QZA:-}"
if [[ -z "$FEATURE_TABLE_QZA" ]]; then FEATURE_TABLE_QZA=$(find "$AMPLISEQ_DIR" -type f -name '*.qza' | grep -Ei 'table|feature' | head -n 1 || true); fi
if [[ -z "$TAXONOMY_QZA" ]]; then TAXONOMY_QZA=$(find "$AMPLISEQ_DIR" -type f -name '*.qza' | grep -Ei 'taxonomy' | head -n 1 || true); fi
if [[ -z "$FEATURE_TABLE_QZA" || -z "$TAXONOMY_QZA" ]]; then echo "Set FEATURE_TABLE_QZA and TAXONOMY_QZA after inspecting *.qza files."; find "$AMPLISEQ_DIR" -type f -name '*.qza' -print | sort; exit 1; fi
qiime tools export --input-path "$FEATURE_TABLE_QZA" --output-path "$OUTDIR/feature_table"
qiime tools export --input-path "$TAXONOMY_QZA" --output-path "$OUTDIR/taxonomy"
qiime diversity alpha --i-table "$FEATURE_TABLE_QZA" --p-metric shannon --o-alpha-diversity "$OUTDIR/shannon.qza"
qiime diversity alpha --i-table "$FEATURE_TABLE_QZA" --p-metric observed_features --o-alpha-diversity "$OUTDIR/observed_features.qza"
echo "Descriptive downstream analysis complete."
