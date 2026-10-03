#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"
TABLE_QZA="$PROJECT/Analysis/ampliseq/<feature-table>.qza"
TAXONOMY_QZA="$PROJECT/Analysis/ampliseq/<taxonomy>.qza"
METADATA="$PROJECT/Metadata/sample-metadata.tsv"
OUT="$PROJECT/Downstream/qiime2"
mkdir -p "$OUT"

test -f "$TABLE_QZA"
test -f "$TAXONOMY_QZA"
test -f "$METADATA"

qiime tools export --input-path "$TABLE_QZA" --output-path "$OUT/feature_table"
qiime tools export --input-path "$TAXONOMY_QZA" --output-path "$OUT/taxonomy"

# Descriptive alpha diversity for the technical-validation sample.
qiime diversity alpha --i-table "$TABLE_QZA" --p-metric shannon --o-alpha-diversity "$OUT/shannon.qza"
qiime diversity alpha --i-table "$TABLE_QZA" --p-metric observed_features --o-alpha-diversity "$OUT/observed_features.qza"

# Beta diversity requires multiple biological samples.
if [[ "${RUN_MULTI_SAMPLE:-false}" == "true" ]]; then
  qiime diversity beta --i-table "$TABLE_QZA" --p-metric braycurtis --o-distance-matrix "$OUT/bray_curtis.qza"
  qiime diversity pcoa --i-distance-matrix "$OUT/bray_curtis.qza" --o-pcoa "$OUT/bray_curtis_pcoa.qza"
  qiime emperor plot --i-pcoa "$OUT/bray_curtis_pcoa.qza" --m-metadata-file "$METADATA" --o-visualization "$OUT/bray_curtis_emperor.qzv"
  qiime taxa barplot --i-table "$TABLE_QZA" --i-taxonomy "$TAXONOMY_QZA" --m-metadata-file "$METADATA" --o-visualization "$OUT/taxa_barplot.qzv"
fi

echo "QIIME 2 downstream stage complete."