#!/usr/bin/env bash
set -euo pipefail

mkdir -p work metadata
curl -fsSL --retry 3 'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA637763' -o work/runinfo.csv

python3 - <<'PY'
import csv, re
from pathlib import Path
rows=list(csv.DictReader(open("work/runinfo.csv",encoding="utf-8")))
keep=[]
for r in rows:
    run=r.get("Run","").strip()
    sample=r.get("SampleName","").strip()
    if not run or not sample: continue
    s=sample.upper()
    if "IBS" in s: label="IBS"
    elif re.search(r"(^|[-_ ])HC($|[-_ ])",s) or "HEALTHY" in s or "CONTROL" in s: label="HC"
    else: continue
    keep.append((sample,run,label,r.get("BioSample",""),r.get("Experiment","")))
if len(keep)<100 or {x[2] for x in keep}!={"IBS","HC"}:
    raise SystemExit(f"Unexpected metadata extraction: {len(keep)} rows; labels={sorted({x[2] for x in keep})}")
with open("metadata/sample-metadata.tsv","w") as f:
    f.write("sample-id\tsra_accession\tgroup\tbiosample\texperiment\n")
    for sample,run,label,bio,exp in keep:
        sid=re.sub(r"[^A-Za-z0-9_.-]","_",sample)
        f.write(f"{sid}\t{run}\t{label}\t{bio}\t{exp}\n")
print("Wrote",len(keep),"samples")
PY
