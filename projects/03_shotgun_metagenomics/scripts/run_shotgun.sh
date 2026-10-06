#!/usr/bin/env bash
set -euo pipefail

PROJECT="PRJNA273761"
RUN_ACCESSION="SRR1779146"
SAMPLE_ACCESSION="SAMN03295851"
EXPERIMENT_ACCESSION="SRX858749"
STUDY_ACCESSION="SRP052967"
INSTRUMENT_PLATFORM="ILLUMINA"
LIBRARY_STRATEGY="WGS"
LIBRARY_LAYOUT="PAIRED"

ROOT="$(cd "$(dirname "\${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$ROOT/work"
RESULTS="$ROOT/results"
mkdir -p "$WORK" "$RESULTS"

R1_URL="https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR177/006/SRR1779146/SRR1779146_1.fastq.gz"
R2_URL="https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR177/006/SRR1779146/SRR1779146_2.fastq.gz"

curl -fL --retry 8 --retry-all-errors --retry-delay 3 "$R1_URL" -o "$WORK/raw_R1.fastq.gz"
curl -fL --retry 8 --retry-all-errors --retry-delay 3 "$R2_URL" -o "$WORK/raw_R2.fastq.gz"

fastp \
  --in1 "$WORK/raw_R1.fastq.gz" \
  --in2 "$WORK/raw_R2.fastq.gz" \
  --out1 "$WORK/clean_R1.fastq.gz" \
  --out2 "$WORK/clean_R2.fastq.gz" \
  --json "$RESULTS/fastp_summary.json" \
  --html "$WORK/fastp.html" \
  --thread 4 \
  --detect_adapter_for_pe

rm -f "$WORK/raw_R1.fastq.gz" "$WORK/raw_R2.fastq.gz"

printf "run_accession\t%s\nstudy_accession\t%s\nsample_accession\t%s\nexperiment_accession\t%s\ninstrument_platform\t%s\nlibrary_strategy\t%s\nlibrary_layout\t%s\nproject_accession\t%s\n" \
  "$RUN_ACCESSION" "$STUDY_ACCESSION" "$SAMPLE_ACCESSION" "$EXPERIMENT_ACCESSION" \
  "$INSTRUMENT_PLATFORM" "$LIBRARY_STRATEGY" "$LIBRARY_LAYOUT" "$PROJECT" > "$RESULTS/run_metadata.tsv"

DB_TGZ="$WORK/k2_standard_08_GB_20260626.tar.gz"
DB_URL="https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08_GB_20260626.tar.gz"
DB_ROOT="$WORK/kraken2_db"

curl -fL --retry 8 --retry-all-errors --retry-delay 5 "$DB_URL" -o "$DB_TGZ"
mkdir -p "$DB_ROOT"
tar -xzf "$DB_TGZ" -C "$DB_ROOT"
rm -f "$DB_TGZ"
DB="$(dirname "$(find "$DB_ROOT" -type f -name 'hash.k2d' -print -quit)")"
test -n "$DB"
test -s "$DB/hash.k2d"
test -s "$DB/opts.k2d"
test -s "$DB/taxo.k2d"

kraken2 \
  --db "$DB" \
  --paired \
  --threads 2 \
  --memory-mapping \
  --gzip-compressed \
  --use-names \
  --report "$RESULTS/kraken2.report" \
  --output "$WORK/kraken2.output" \
  "$WORK/clean_R1.fastq.gz" "$WORK/clean_R2.fastq.gz"

rm -rf "$DB_ROOT" "$WORK/kraken2.output"

CENT_DB_DIR="$WORK/centrifuge_db"
CENT_TGZ="$WORK/p_compressed+h+v.tar.gz"
CENT_URL="https://genome-idx.s3.amazonaws.com/centrifuge/p_compressed%2Bh%2Bv.tar.gz"
mkdir -p "$CENT_DB_DIR"
curl -fL --retry 8 --retry-all-errors --retry-delay 5 "$CENT_URL" -o "$CENT_TGZ"
tar -xzf "$CENT_TGZ" -C "$CENT_DB_DIR"
rm -f "$CENT_TGZ"

CENT_INDEX="$(find "$CENT_DB_DIR" -maxdepth 1 -type f -name '*.1.cf' -print -quit | sed 's/\.1\.cf$//')"
test -n "$CENT_INDEX"

centrifuge \
  -x "$CENT_INDEX" \
  -1 "$WORK/clean_R1.fastq.gz" \
  -2 "$WORK/clean_R2.fastq.gz" \
  -p 4 \
  -S "$RESULTS/centrifuge.classification.tsv" \
  --report-file "$RESULTS/centrifuge.report.tsv"

python3 "$ROOT/scripts/summarize_kraken.py" \
  "$RESULTS/kraken2.report" "$RESULTS/top_taxa.tsv" \
  "$RESULTS/REPORT.md" "$RESULTS/run_metadata.tsv"

python3 "$ROOT/scripts/compare_classifiers.py" \
  "$RESULTS/kraken2.report" "$RESULTS/centrifuge.report.tsv" \
  "$RESULTS/classifier_comparison.tsv"

rm -f "$RESULTS/centrifuge.classification.tsv"
rm -rf "$WORK"

echo "Project 03 completed successfully with Kraken2 and Centrifuge."
