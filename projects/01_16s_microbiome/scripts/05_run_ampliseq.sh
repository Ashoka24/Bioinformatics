#!/usr/bin/env bash
set -euo pipefail
DATA_ROOT="${DATA_ROOT:-/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
PARAMS_FILE="${PARAMS_FILE:-$(cd "$(dirname "$0")/.." && pwd)/params/ampliseq_params.json}"
WORK_DIR="$PROJECT_DIR/work_dir/ampliseq"
LOG_FILE="$PROJECT_DIR/Logs/ampliseq.log"
mkdir -p "$WORK_DIR" "$PROJECT_DIR/Logs"
nextflow run nf-core/ampliseq -r 2.11.0 -name NCBI_Gut_SRR26534086 -work-dir "$WORK_DIR" -params-file "$PARAMS_FILE" -profile docker -resume 2>&1 | tee "$LOG_FILE"
echo "Pipeline finished. Log: $LOG_FILE"
