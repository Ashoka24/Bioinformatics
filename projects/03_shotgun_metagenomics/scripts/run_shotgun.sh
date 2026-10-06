#!/usr/bin/env bash
set -euo pipefail

PROJECT="PRJNA786061"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$ROOT/work"
RESULTS="$ROOT/results"
DB="$WORK/minikraken2_v2_8GB"
mkdir -p "$WORK" "$RESULTS"

API="https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=study_accession=%22${PROJECT}%22%20AND%20library_strategy=%22WGS%22%20AND%20library_layout=%22PAIRED%22&fields=run_accession,study_accession,sample_accession,experiment_accession,instrument_platform,library_strategy,library_layout,fastq_ftp,fastq_bytes&format=tsv&limit=1"

curl -fsSL --retry 8 --retry-all-errors --retry-delay 3 "$API" > "$WORK/ena.tsv"
test "$(wc -l < "$WORK/ena.tsv")" -ge 2

python3 - "$WORK/ena.tsv" "$WORK/run.env" <<'PY'
import csv, sys
src, out = sys.argv[1:]
with open(src, newline="") as f:
    row = next(csv.DictReader(f, delimiter="\t"))
with open(out, "w") as w:
    for key in ["run_accession","study_accession","sample_accession","experiment_accession",
                "instrument_platform","library_strategy","library_layout","fastq_ftp","fastq_bytes"]:
        w.write(f'{key.upper()}="{row.get(key,"")}"\n')
PY

source "$WORK/run.env"
echo "Selected run: $RUN_ACCESSION"

IFS=';' read -r FTP1 FTP2 <<< "$FASTQ_FTP"
curl -fL --retry 8 --retry-all-errors --retry-delay 3 "https://$FTP1" -o "$WORK/raw_R1.fastq.gz"
curl -fL --retry 8 --retry-all-errors --retry-delay 3 "https://$FTP2" -o "$WORK/raw_R2.fastq.gz"

fastp --in1 "$WORK/raw_R1.fastq.gz" --in2 "$WORK/raw_R2.fastq.gz"   --out1 "$WORK/clean_R1.fastq.gz" --out2 "$WORK/clean_R2.fastq.gz"   --json "$RESULTS/fastp_summary.json" --html "$WORK/fastp.html"   --thread 4 --detect_adapter_for_pe

DB_TGZ="$WORK/minikraken2_v2_8GB.tgz"
DB_URL="https://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/old/minikraken2_v2_8GB_201904_UPDATE.tgz"

if [ ! -d "$DB" ]; then
  curl -fL --retry 5 --retry-all-errors --retry-delay 5 "$DB_URL" -o "$DB_TGZ"
  tar -xzf "$DB_TGZ" -C "$WORK"
  FOUND="$(find "$WORK" -maxdepth 1 -type d -name 'minikraken2_v2_8GB*' | head -n1)"
  test -n "$FOUND"
  mv "$FOUND" "$DB"
fi

kraken2 --db "$DB" --paired --threads 4 --gzip-compressed --use-names   --report "$RESULTS/kraken2.report" --output "$WORK/kraken2.output"   "$WORK/clean_R1.fastq.gz" "$WORK/clean_R2.fastq.gz"

printf "run_accession\t%s\nstudy_accession\t%s\nsample_accession\t%s\nexperiment_accession\t%s\ninstrument_platform\t%s\nlibrary_strategy\t%s\nlibrary_layout\t%s\nfastq_bytes\t%s\n"   "$RUN_ACCESSION" "$STUDY_ACCESSION" "$SAMPLE_ACCESSION" "$EXPERIMENT_ACCESSION"   "$INSTRUMENT_PLATFORM" "$LIBRARY_STRATEGY" "$LIBRARY_LAYOUT" "$FASTQ_BYTES" > "$RESULTS/run_metadata.tsv"

python3 "$ROOT/scripts/summarize_kraken.py"   "$RESULTS/kraken2.report" "$RESULTS/top_taxa.tsv"   "$RESULTS/REPORT.md" "$RESULTS/run_metadata.tsv"

rm -rf "$WORK"
echo "Project 03 completed successfully."
