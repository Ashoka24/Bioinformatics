#!/usr/bin/env python3
"""Resolve GEO sample accessions to SRA run accessions for Project 07."""

from pathlib import Path
import csv

from pysradb.sraweb import SRAweb

STUDY = "SRP326537"
TARGETS = {
    "GSM5413848": "N1001",
    "GSM5413849": "T1001",
}

out = Path("work")
out.mkdir(exist_ok=True)
metadata = SRAweb().metadata(STUDY, detailed=True)

if metadata is None or len(metadata) == 0:
    raise SystemExit("No SRA metadata returned for SRP326537")

columns = {str(c).lower(): c for c in metadata.columns}
gsm_column = next((columns[c] for c in ("geo_accession", "geo_sample", "sample_accession") if c in columns), None)
run_column = next((columns[c] for c in ("run", "run_accession") if c in columns), None)

if gsm_column is None or run_column is None:
    raise SystemExit(f"Could not identify GEO/run columns. Available: {list(metadata.columns)}")

rows = []
for gsm, sample in TARGETS.items():
    hits = metadata[metadata[gsm_column].astype(str).str.contains(gsm, na=False)]
    if hits.empty:
        raise SystemExit(f"No SRA run found for {gsm}")
    for _, row in hits.iterrows():
        rows.append({"sample": sample, "geo": gsm, "run": row[run_column]})

with open(out / "selected_sra_runs.tsv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["sample", "geo", "run"], delimiter="	")
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {out / 'selected_sra_runs.tsv'}")
for row in rows:
    print(f"{row['geo']}	{row['sample']}	{row['run']}")
