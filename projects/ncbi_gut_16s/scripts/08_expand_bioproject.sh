#!/usr/bin/env bash
set -euo pipefail

PROJECT="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/NCBI_Gut_16S"
BIOPROJECT="PRJNA1031545"

mkdir -p "$PROJECT/Metadata"

# Requires Entrez Direct (edirect).
esearch -db sra -query "$BIOPROJECT" |
  efetch -format runinfo |
  tee "$PROJECT/Metadata/$BIOPROJECT_runinfo.csv"

python3 - "$PROJECT/Metadata/$BIOPROJECT_runinfo.csv" <<'PY'
import csv
import sys

src = sys.argv[1]
with open(src, newline="") as fh:
    rows = csv.DictReader(fh)
    runs = [row["Run"] for row in rows if row.get("Run")]

print("Public runs discovered:", len(runs))
print("First 20:")
for run in runs[:20]:
    print(run)
PY

echo "Review the run metadata before downloading the cohort."
