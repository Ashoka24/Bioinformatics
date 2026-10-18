#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

RUN=SRR26534086
IMAGE=quay.io/qiime2/amplicon:2024.10
mkdir -p work/raw work/q2 results_actual/qc results_actual/tables

curl -fsSL --retry 3 \
    "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=$RUN&result=read_run&fields=run_accession,fastq_ftp,fastq_md5,fastq_bytes&format=tsv" \
    > work/ena.tsv

IFS=$'\t' read -r _ FASTQ_URLS FASTQ_MD5S _ < <(tail -n 1 work/ena.tsv)
IFS=';' read -r -a URLS <<< "$FASTQ_URLS"
IFS=';' read -r -a MD5S <<< "$FASTQ_MD5S"
if [[ ${#URLS[@]} -ne 2 || ${#MD5S[@]} -ne 2 ]]; then
    echo "ERROR: expected two FASTQ URLs and two MD5 checksums for $RUN." >&2
    cat work/ena.tsv >&2
    exit 1
fi

for index in 0 1; do
    url="${URLS[$index]#ftp://}"
    filename="$(basename "$url")"
    destination="work/raw/$filename"
    curl -fL --retry 3 "https://$url" -o "$destination"
    printf '%s  %s\n' "${MD5S[$index]}" "$destination" | md5sum -c -
done

R1="work/raw/${RUN}_1.fastq.gz"
R2="work/raw/${RUN}_2.fastq.gz"
[[ -s "$R1" && -s "$R2" ]] || {
    echo "ERROR: expected paired FASTQ files were not downloaded for $RUN." >&2
    ls -lh work/raw >&2
    exit 1
}

cat > work/manifest.tsv <<EOF
sample-id	forward-absolute-filepath	reverse-absolute-filepath
$RUN	/data/$R1	/data/$R2
EOF

docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools import \
    --type 'SampleData[PairedEndSequencesWithQuality]' \
    --input-path /data/work/manifest.tsv \
    --input-format PairedEndFastqManifestPhred33V2 \
    --output-path /data/work/q2/demux.qza

docker run --rm -v "$PWD:/data" "$IMAGE" qiime cutadapt trim-paired \
    --i-demultiplexed-sequences /data/work/q2/demux.qza \
    --p-front-f CCTACGGGNGGCWGCAG \
    --p-front-r GACTACHVGGGTATCTAATCC \
    --p-error-rate 0.1 \
    --p-no-discard-untrimmed \
    --o-trimmed-sequences /data/work/q2/trimmed.qza

docker run --rm -v "$PWD:/data" "$IMAGE" qiime deblur denoise-16S \
    --i-demultiplexed-seqs /data/work/q2/trimmed.qza \
    --p-trim-length 200 \
    --p-sample-stats \
    --p-jobs-to-start 2 \
    --o-table /data/work/q2/table.qza \
    --o-representative-sequences /data/work/q2/rep-seqs.qza \
    --o-stats /data/work/q2/deblur-stats.qza

curl -fL --retry 3 \
    https://data.qiime2.org/classifiers/sklearn-1.4.2/silva/silva-138-99-nb-classifier.qza \
    -o work/silva.qza
echo 'c08a1aa4d56b449b511f7215543a43249ae9c54b57491428a7e5548a62613616  work/silva.qza' | sha256sum -c -

docker run --rm -v "$PWD:/data" "$IMAGE" qiime feature-classifier classify-sklearn \
    --i-classifier /data/work/silva.qza \
    --i-reads /data/work/q2/rep-seqs.qza \
    --p-n-jobs 2 \
    --o-classification /data/work/q2/taxonomy.qza

for artifact in deblur-stats table rep-seqs taxonomy; do
    docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools export \
        --input-path "/data/work/q2/$artifact.qza" \
        --output-path "/data/results_actual/qc/$artifact"
done

docker run --rm -v "$PWD:/data" "$IMAGE" biom convert \
    -i /data/results_actual/qc/table/feature-table.biom \
    -o /data/results_actual/tables/feature-table.tsv --to-tsv
cp results_actual/qc/taxonomy/taxonomy.tsv results_actual/tables/taxonomy.tsv

for metric in observed_features shannon simpson; do
    docker run --rm -v "$PWD:/data" "$IMAGE" qiime diversity alpha \
        --i-table /data/work/q2/table.qza \
        --p-metric "$metric" \
        --o-alpha-diversity "/data/work/q2/$metric.qza"
    docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools export \
        --input-path "/data/work/q2/$metric.qza" \
        --output-path "/data/results_actual/tables/$metric"
done

python3 16s-gut-microbiome/scripts/08_build_actual_results.py
