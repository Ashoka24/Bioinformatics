#!/usr/bin/env bash
set -euo pipefail

DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
PARAMS_FILE="${PARAMS_FILE:-$(cd "$(dirname "$0")/.." && pwd)/params/ampliseq_params.json}"
WORK_DIR="$PROJECT_DIR/work_dir/ampliseq"
LOG_DIR="$PROJECT_DIR/logs"
RUNTIME_PARAMS="$LOG_DIR/ampliseq_params.runtime.json"
LOG_FILE="$LOG_DIR/ampliseq.log"

mkdir -p "$WORK_DIR" "$LOG_DIR"

# Keep the tracked parameter file readable, but rewrite its local data root at runtime.
sed "s#/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data/16s_ncbi_gut#$PROJECT_DIR#g"     "$PARAMS_FILE" > "$RUNTIME_PARAMS"

nextflow run nf-core/ampliseq \
    -r 2.11.0 \
    -name NCBI_Gut_SRR26534086 \
    -work-dir "$WORK_DIR" \
    -params-file "$RUNTIME_PARAMS" \
    -profile docker \
    -resume \
    2>&1 | tee "$LOG_FILE"

echo "Pipeline finished. Log: $LOG_FILE"
