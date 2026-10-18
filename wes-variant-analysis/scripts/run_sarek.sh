#!/usr/bin/env bash
set -euo pipefail

# Run the pinned nf-core/sarek WES tumor-normal workflow.
# Run this script from any directory; paths are resolved from this file.

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

INPUT="${INPUT:-config/samplesheet.csv}"
OUTDIR="${OUTDIR:-results}"
SAREK_VERSION="${SAREK_VERSION:-3.10.0}"
GENOME="${GENOME:-GATK.GRCh38}"

command -v python3 >/dev/null || { echo "Python 3 is required for samplesheet validation." >&2; exit 1; }
command -v nextflow >/dev/null || { echo "Nextflow is required." >&2; exit 1; }
command -v docker >/dev/null || { echo "Docker is required for -profile docker." >&2; exit 1; }
[[ -f "$INPUT" ]] || { echo "Samplesheet not found: $INPUT" >&2; exit 1; }

echo "Validating samplesheet and input FASTQs..."
python3 scripts/validate_samplesheet.py --samplesheet "$INPUT" --check-files

echo "Running nf-core/sarek $SAREK_VERSION"
echo "Input: $INPUT"
echo "Output: $OUTDIR"
echo "Reference: $GENOME"

nextflow run nf-core/sarek -r "$SAREK_VERSION" \
  -profile docker \
  --input "$INPUT" \
  --outdir "$OUTDIR" \
  --genome "$GENOME" \
  --wes \
  --tools mutect2,vep \
  -resume
