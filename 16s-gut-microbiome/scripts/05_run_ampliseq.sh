#!/usr/bin/env bash
set -euo pipefail

DATA_ROOT="${DATA_ROOT:-$HOME/bioinformatics-data}"
PROJECT_DIR="${PROJECT_DIR:-$DATA_ROOT/16s_ncbi_gut}"
ACCESSION="${ACCESSION:-SRR26534086}"
PARAMS_FILE="${PARAMS_FILE:-$(cd "$(dirname "$0")/.." && pwd)/params/ampliseq_params.json}"
WORK_DIR="$PROJECT_DIR/work_dir/ampliseq"
LOG_DIR="$PROJECT_DIR/Logs"
RUNTIME_PARAMS="$LOG_DIR/ampliseq_params.runtime.json"
LOG_FILE="$LOG_DIR/ampliseq.log"
INPUT_DIR="$PROJECT_DIR/RawData/$ACCESSION/input"
OUT_DIR="$PROJECT_DIR/Analysis/ampliseq"

mkdir -p "$WORK_DIR" "$LOG_DIR" "$OUT_DIR"

if [[ ! -d "$INPUT_DIR" ]] || ! compgen -G "$INPUT_DIR/*.fastq.gz" >/dev/null; then
    echo "ERROR: no compressed FASTQ files found in $INPUT_DIR" >&2
    echo "Run scripts/01_download_ncbi.sh and scripts/04_prepare_input.sh first." >&2
    exit 1
fi

# Keep the tracked configuration portable; resolve local paths only at runtime.
python3 - "$PARAMS_FILE" "$RUNTIME_PARAMS" "$INPUT_DIR" "$OUT_DIR" <<'PY'
import json
import sys
from pathlib import Path

source, destination, input_dir, output_dir = sys.argv[1:]
try:
    params = json.loads(Path(source).read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    raise SystemExit(f"Could not read parameter file {source}: {exc}")

params["input_folder"] = str(Path(input_dir).resolve()) + "/"
params["outdir"] = str(Path(output_dir).resolve()) + "/"
Path(destination).write_text(json.dumps(params, indent=2) + "\n", encoding="utf-8")
PY

nextflow run nf-core/ampliseq \
    -r 2.11.0 \
    -name "NCBI_Gut_$ACCESSION" \
    -work-dir "$WORK_DIR" \
    -params-file "$RUNTIME_PARAMS" \
    -profile docker \
    -resume \
    2>&1 | tee "$LOG_FILE"

echo "Pipeline finished. Log: $LOG_FILE"
