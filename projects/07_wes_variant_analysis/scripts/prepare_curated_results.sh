#!/usr/bin/env bash
# Curate lightweight WES deliverables for GitHub. This script does NOT commit or push.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

RESULTS="results/hcc1395_sarek"
[[ -d "$RESULTS" ]] || { echo "ERROR: $RESULTS not found. Run this inside projects/07_wes_variant_analysis."; exit 1; }

files=()

# FastQC HTML only; raw FASTQ and bulky ZIP bundles are deliberately excluded.
while IFS= read -r -d '' f; do files+=("$f"); done < <(
  find "$RESULTS/preprocessing" -type f -iname '*fastqc.html' -size -10M -print0 2>/dev/null || true
)

# MultiQC HTML.
while IFS= read -r -d '' f; do files+=("$f"); done < <(
  find "$RESULTS" -type f -iname '*multiqc*.html' -size -10M -print0 2>/dev/null || true
)

# Small result/summary tables only; do not sweep all results directories.
if [[ -d "$RESULTS/csv" ]]; then
  while IFS= read -r -d '' f; do files+=("$f"); done < <(
    find "$RESULTS/csv" -type f \( -iname '*.csv' -o -iname '*.tsv' \) -size -10M -print0
  )
fi

# Final filtered VEP-annotated VCF only (not intermediate/unfiltered VCFs).
vcfs=()
while IFS= read -r -d '' f; do
  vcfs+=("$f")
  files+=("$f")
done < <(
  find "$RESULTS/annotation" -type f -iname '*filtered_vep*.vcf.gz' -size -95M -print0 2>/dev/null || true
)

# Add the index only for the selected final VCF.
for vcf in "${vcfs[@]}"; do
  [[ -f "${vcf}.tbi" && $(stat -c %s "${vcf}.tbi") -lt 99614720 ]] && files+=("${vcf}.tbi")
done

# Small Nextflow HTML execution reports, when available.
while IFS= read -r -d '' f; do files+=("$f"); done < <(
  find "$RESULTS/pipeline_info" -type f \( -iname '*execution_report.html' -o -iname '*execution_timeline.html' \) -size -10M -print0 2>/dev/null || true
)

# Remove duplicate paths.
mapfile -t files < <(printf '%s\n' "${files[@]}" | awk 'NF && !seen[$0]++' | sort)

manifest="$RESULTS/PORTFOLIO_MANIFEST.tsv"
summary="$RESULTS/PORTFOLIO_SUMMARY.md"
mkdir -p "$RESULTS"

{
  printf 'path\tsize_bytes\tsha256\n'
  for f in "${files[@]}"; do
    [[ -f "$f" ]] || continue
    size=$(stat -c %s "$f")
    sha=$(sha256sum "$f" | awk '{print $1}')
    printf '%s\t%s\t%s\n' "$f" "$size" "$sha"
  done
} > "$manifest"

vcf_records="Not available"
vcf_gzip="Not checked"
vep_csq="Not checked"
vcf_index="Not found"
if (("${#vcfs[@]}" > 0)); then
  vcf="${vcfs[0]}"
  if gzip -t "$vcf"; then vcf_gzip="PASS"; else vcf_gzip="FAIL"; fi
  vcf_records=$(zgrep -vc '^#' "$vcf" || true)
  if zgrep -q -m1 '^##INFO=<ID=CSQ' "$vcf"; then vep_csq="Present"; else vep_csq="Not detected"; fi
  [[ -f "${vcf}.tbi" ]] && vcf_index="Present (index query not tested)"
fi

fastqc_count=$(find "$RESULTS/preprocessing" -type f -iname '*fastqc.html' 2>/dev/null | wc -l)
multiqc_count=$(find "$RESULTS" -type f -iname '*multiqc*.html' 2>/dev/null | wc -l)
table_count=0
[[ -d "$RESULTS/csv" ]] && table_count=$(find "$RESULTS/csv" -type f \( -iname '*.csv' -o -iname '*.tsv' \) -size -10M 2>/dev/null | wc -l)

cat > "$summary" <<EOF
# HCC1395 WES — Portfolio Results Summary

## Execution context

- Workflow: nf-core/sarek 3.10.0 with Nextflow and Docker
- Pair label: HCC1395_vs_HCC1395BL
- Reference: GATK GRCh38
- Variant caller: Mutect2
- Annotation: Ensembl VEP
- Scope: computational workflow validation; not clinical interpretation

## Available deliverables detected locally

- FastQC HTML reports: $fastqc_count
- MultiQC HTML reports: $multiqc_count
- Small CSV/TSV result tables in results/csv: $table_count
- Final filtered VEP-annotated VCF candidates selected: ${#vcfs[@]}

## Final VCF checks

- Non-header VCF records: $vcf_records
- gzip integrity: $vcf_gzip
- VEP CSQ header: $vep_csq
- Tabix index: $vcf_index

A present index is not proof that indexed queries work. The script does not claim index-query validation, clinical significance, or biological conclusions. Inspect the selected tables before describing them as a sample comparison.

## File manifest

See [PORTFOLIO_MANIFEST.tsv](PORTFOLIO_MANIFEST.tsv) for the selected file paths, byte sizes, and SHA-256 checksums.

## Excluded from GitHub

Raw FASTQ/SRA data, BAM/CRAM files, large intermediate results, reference assets, Nextflow work/cache directories, credentials, and machine-specific configuration are intentionally excluded.
EOF

# Stage only curated outputs and generated documentation. Do not stage the whole results directory.
git add -- "$manifest" "$summary"
for f in "${files[@]}"; do
  [[ -f "$f" ]] && git add -- "$f"
done

# Include the small reusable parameters file only if it parses as JSON.
if [[ -f config/sarek_params.json ]] && python3 -m json.tool config/sarek_params.json >/dev/null 2>&1; then
  git add -- config/sarek_params.json
fi

echo
echo "Curated files have been STAGED, not committed or pushed."
echo "Review the exact staged file list and size summary below:"
git diff --cached --name-only
echo
git diff --cached --stat
echo
echo "Next: run 'git diff --cached --check' and inspect the staged files before committing."
