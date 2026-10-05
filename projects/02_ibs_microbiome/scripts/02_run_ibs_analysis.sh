#!/usr/bin/env bash
set -euo pipefail

IMAGE=quay.io/qiime2/amplicon:2024.10
mkdir -p work/raw work/q2 results_actual/qc results_actual/tables results_actual/ml
rm -rf results_actual/qc/* results_actual/tables/* results_actual/ml/*

bash projects/02_ibs_microbiome/scripts/01_prepare_metadata.sh

python3 - <<'PY'
import csv,subprocess
from pathlib import Path

meta=list(csv.DictReader(open("metadata/sample-metadata.tsv"),delimiter="\t"))
raw=Path("work/raw"); raw.mkdir(parents=True,exist_ok=True)

for i,r in enumerate(meta,1):
    run=r["sra_accession"]
    url=f"https://www.ebi.ac.uk/ena/portal/api/filereport?accession={run}&result=read_run&fields=run_accession,fastq_ftp&format=tsv"
    report=raw / f"{run}.ena.tsv"
    subprocess.run([
        "curl","-fsSL","--retry","8","--retry-all-errors","--retry-delay","3",
        "--connect-timeout","30","--max-time","120",url,"-o",str(report)
    ],check=True)
    lines=report.read_text().strip().splitlines()
    if len(lines)<2:
        raise SystemExit(f"No ENA FASTQ record for {run}")
    for ftp in lines[1].split("\t")[1].split(";"):
        name=Path(ftp).name
        dest=raw/name
        if not dest.exists():
            subprocess.run([
                "curl","-fL","--retry","8","--retry-all-errors","--retry-delay","3",
                "--connect-timeout","30","--max-time","600",
                "https://"+ftp.removeprefix("ftp://"),"-o",str(dest)
            ],check=True)
    if i%10==0:
        print(f"Resolved {i}/{len(meta)}")
PY

python3 - <<'PY'
import csv
meta=list(csv.DictReader(open("metadata/sample-metadata.tsv"),delimiter="\t"))
with open("work/manifest.tsv","w") as f:
    f.write("sample-id\tforward-absolute-filepath\treverse-absolute-filepath\n")
    for r in meta:
        run=r["sra_accession"]
        f.write(f"{r['sample-id']}\t/data/work/raw/{run}_1.fastq.gz\t/data/work/raw/{run}_2.fastq.gz\n")
with open("work/forward-manifest.tsv","w") as f:
    f.write("sample-id\tabsolute-filepath\n")
    for r in meta:
        f.write(f"{r['sample-id']}\t/data/work/raw/{r['sra_accession']}_1.fastq.gz\n")
PY

docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools import --type 'SampleData[SequencesWithQuality]' --input-path /data/work/forward-manifest.tsv --input-format SingleEndFastqManifestPhred33V2 --output-path /data/work/q2/forward.qza
docker run --rm -v "$PWD:/data" "$IMAGE" qiime demux summarize --i-data /data/work/q2/forward.qza --o-visualization /data/work/q2/demux.qzv
docker run --rm -v "$PWD:/data" "$IMAGE" qiime cutadapt trim-single --i-demultiplexed-sequences /data/work/q2/forward.qza --p-front "AGRGTTTGATYMTGGCTCAG" --p-error-rate 0.15 --p-discard-untrimmed --o-trimmed-sequences /data/work/q2/trimmed-forward.qza
docker run --rm -v "$PWD:/data" "$IMAGE" qiime deblur denoise-16S --i-demultiplexed-seqs /data/work/q2/trimmed-forward.qza --p-trim-length 200 --p-sample-stats --p-jobs-to-start 2 --o-table /data/work/q2/table.qza --o-representative-sequences /data/work/q2/rep-seqs.qza --o-stats /data/work/q2/deblur-stats.qza

curl -fL --retry 5 --retry-all-errors --retry-delay 3 https://data.qiime2.org/classifiers/sklearn-1.4.2/silva/silva-138-99-nb-classifier.qza -o work/silva.qza
echo 'c08a1aa4d56b449b511f7215543a43249ae9c54b57491428a7e5548a62613616  work/silva.qza' | sha256sum -c -

docker run --rm -v "$PWD:/data" "$IMAGE" qiime feature-classifier classify-sklearn --i-classifier /data/work/silva.qza --i-reads /data/work/q2/rep-seqs.qza --p-n-jobs 2 --o-classification /data/work/q2/taxonomy.qza

for pair in "deblur-stats deblur-stats" "table table" "rep-seqs rep-seqs" "taxonomy taxonomy"; do
  set -- $pair
  docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools export --input-path "/data/work/q2/$1.qza" --output-path "/data/results_actual/qc/$2"
done

docker run --rm -v "$PWD:/data" "$IMAGE" biom convert -i /data/results_actual/qc/table/feature-table.biom -o /data/results_actual/tables/feature-table.tsv --to-tsv
cp results_actual/qc/taxonomy/taxonomy.tsv results_actual/tables/taxonomy.tsv

for metric in observed_features shannon simpson; do
  docker run --rm -v "$PWD:/data" "$IMAGE" qiime diversity alpha --i-table /data/work/q2/table.qza --p-metric "$metric" --o-alpha-diversity "/data/work/q2/$metric.qza"
  docker run --rm -v "$PWD:/data" "$IMAGE" qiime tools export --input-path "/data/work/q2/$metric.qza" --output-path "/data/results_actual/tables/$metric"
done

python3 projects/02_ibs_microbiome/scripts/03_build_results.py
