#!/usr/bin/env bash
set -euo pipefail

# Project 07: retrieve the selected public NCBI/SRA WES pair.
# Resolve run accessions first with resolve_sra_runs.py.

OUTDIR="${OUTDIR:-work/fastq}"
RUNS_TSV="${RUNS_TSV:-work/selected_sra_runs.tsv}"

mkdir -p "$OUTDIR"

if [[ ! -s "$RUNS_TSV" ]]; then
  echo "Missing $RUNS_TSV. Run: python scripts/resolve_sra_runs.py" >&2
  exit 1
fi

normal_run="$(awk -F "\t" '$1 == "N1001" {print $3; exit}' "$RUNS_TSV")"
tumor_run="$(awk -F "\t" '$1 == "T1001" {print $3; exit}' "$RUNS_TSV")"
[[ -n "$normal_run" ]] || { echo "No N1001 run found in $RUNS_TSV" >&2; exit 1; }
[[ -n "$tumor_run" ]] || { echo "No T1001 run found in $RUNS_TSV" >&2; exit 1; }

download_pair() {
  local run="$1"
  local prefix="$2"
  prefetch "$run"
  fasterq-dump "$run" --split-files --gzip --outdir "$OUTDIR"
  mv "$OUTDIR/${run}_1.fastq.gz" "$OUTDIR/${prefix}_R1.fastq.gz"
  mv "$OUTDIR/${run}_2.fastq.gz" "$OUTDIR/${prefix}_R2.fastq.gz"
}

download_pair "$normal_run" "N1001"
download_pair "$tumor_run" "T1001"

echo "FASTQ files written to $OUTDIR"
