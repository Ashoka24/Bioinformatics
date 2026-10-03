#!/usr/bin/env bash
set -euo pipefail

echo "=== 16S PUBLIC DATA WORKFLOW: ENVIRONMENT CHECK ==="
echo

echo "[System]"
uname -a
echo

echo "[CPU]"
nproc || true
echo

echo "[Memory]"
free -h || true
echo

echo "[Disk]"
df -h "$HOME" || true
echo

for tool in prefetch fasterq-dump vdb-validate fastqc multiqc nextflow docker qiime; do
    if command -v "$tool" >/dev/null 2>&1; then
        printf "%-16s " "$tool"
        case "$tool" in
            fastqc) fastqc --version 2>&1 | head -n 1 ;;
            multiqc) multiqc --version 2>&1 | head -n 1 ;;
            nextflow) nextflow -version 2>&1 | tail -n 1 ;;
            docker) docker --version ;;
            qiime) qiime --version 2>&1 | head -n 1 ;;
            *) "$tool" --version 2>&1 | head -n 1 || true ;;
        esac
    else
        echo "MISSING          $tool"
    fi
done

echo
echo "Windows data folder:"
echo "C:\\Users\\ashok\\OneDrive\\Desktop\\Ashoka\\data"
echo
echo "WSL equivalent:"
echo "/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data"
