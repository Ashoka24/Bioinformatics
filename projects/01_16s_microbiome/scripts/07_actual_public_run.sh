#!/usr/bin/env bash
set -euo pipefail
RUN=SRR26534086
IMAGE=quay.io/qiime2/amplicon:2024.10
mkdir -p work/raw work/q2 results_actual/qc results_actual/tables
curl -fsSL --retry 3 "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=$RUN&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv" > work/ena.tsv
awk -F'\t' 'NR==2 {print $2}' work/ena.tsv | tr ';' '\n' | while read -r url; do f=$(basename "$url"); curl -fL --retry 3 "https://${url#ftp://}" -o "work/raw/$f"; done
cat > work/manifest.tsv <<'EOF'
sample-id	forward-absolute-filepath	reverse-absolute-filepath
SRR26534086	/data/work/raw/SRR26534086_1.fastq.gz	/data/work/raw/SRR26534086_2.fastq.gz
EOF
docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools import --type 'SampleData[PairedEndSequencesWithQuality]' --input-path /data/work/manifest.tsv --input-format PairedEndFastqManifestPhred33V2 --output-path /data/work/q2/demux.qza
docker run --rm -v "$PWD:/data" "$IMAGE" qiime cutadapt trim-paired --i-demultiplexed-sequences /data/work/q2/demux.qza --p-front-f CCTACGGGNGGCWGCAG --p-front-r GACTACHVGGGTATCTAATCC --p-error-rate 0.1 --p-no-discard-untrimmed --o-trimmed-sequences /data/work/q2/trimmed.qza
docker run --rm -v "$PWD:/data" "$IMAGE" qiime deblur denoise-16S --i-demultiplexed-seqs /data/work/q2/trimmed.qza --p-trim-length 200 --p-sample-stats --p-jobs-to-start 2 --o-table /data/work/q2/table.qza --o-representative-sequences /data/work/q2/rep-seqs.qza --o-stats /data/work/q2/deblur-stats.qza
curl -fL --retry 3 https://data.qiime2.org/classifiers/sklearn-1.4.2/silva/silva-138-99-nb-classifier.qza -o work/silva.qza
echo 'c08a1aa4d56b449b511f7215543a43249ae9c54b57491428a7e5548a62613616  work/silva.qza' | sha256sum -c -
docker run --rm -v "$PWD:/data" "$IMAGE" qiime feature-classifier classify-sklearn --i-classifier /data/work/silva.qza --i-reads /data/work/q2/rep-seqs.qza --p-n-jobs 2 --o-classification /data/work/q2/taxonomy.qza
for pair in "deblur-stats deblur-stats" "table table" "rep-seqs rep-seqs" "taxonomy taxonomy"; do set -- $pair; docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools export --input-path "/data/work/q2/$1.qza" --output-path "/data/results_actual/qc/$2"; done
docker run --rm -v "$PWD:/data" "$IMAGE" biom convert -i /data/results_actual/qc/table/feature-table.biom -o /data/results_actual/tables/feature-table.tsv --to-tsv
cp results_actual/qc/taxonomy/taxonomy.tsv results_actual/tables/taxonomy.tsv
for metric in observed_features shannon simpson; do docker run --rm -v "$PWD:/data" "$IMAGE" qiime diversity alpha --i-table /data/work/q2/table.qza --p-metric "$metric" --o-alpha-diversity "/data/work/q2/$metric.qza"; docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools export --input-path "/data/work/q2/$metric.qza" --output-path "/data/results_actual/tables/$metric"; done
python3 projects/01_16s_microbiome/scripts/08_build_actual_results.py