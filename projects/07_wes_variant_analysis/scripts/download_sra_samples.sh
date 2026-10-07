#!/usr/bin/env bash
set -euo pipefail

# Project 07: retrieve the selected public NCBI/SRA WES pair.
# Requires SRA Toolkit. Resolve run accessions from SRP326537 first.

OUTDIR="${1:-work/fastq}"
NORMAL_SRR="${NORMAL_SRR:?Set NORMAL_SRR to the NCBI run accession}"
TUMOR_SRR="${TUMOR_SRR:?Set TUMOR_SRR to the NCBI run accession}"

mkdir -p "$OUTDIR"

prefetch "$NORMAL_SRR"
prefetch "$TUMOR_SRR"

fasterq-dump "$NORMAL_SRR" --split-files --gzip --outdir "$OUTDIR"
fasterq-dump "$TUMOR_SRR" --split-files --gzip --outdir "$OUTDIR"

mv "$OUTDIR/${NORMAL_SRR}_1.fastq.gz" "$OUTDIR/N1001_R1.fastq.gz"
mv "$OUTDIR/${NORMAL_SRR}_2.fastq.gz" "$OUTDIR/N1001_R2.fastq.gz"
mv "$OUTDIR/${TUMOR_SRR}_1.fastq.gz" "$OUTDIR/T1001_R1.fastq.gz"
mv "$OUTDIR/${TUMOR_SRR}_2.fastq.gz" "$OUTDIR/T1001_R2.fastq.gz"
