#!/usr/bin/env bash
set -euo pipefail

echo "=== SYSTEM ==="
uname -a
echo

echo "=== CPU / RAM ==="
nproc
free -h
echo

echo "=== STORAGE ==="
df -h
echo

echo "=== SOFTWARE ==="
docker --version || true
docker info >/dev/null 2>&1 && echo "Docker daemon: OK" || echo "Docker daemon: NOT AVAILABLE"
nextflow -version || true
java -version || true
python3 --version || true
prefetch --version || true
fasterq-dump --version || true
fastqc --version || true
multiqc --version || true
