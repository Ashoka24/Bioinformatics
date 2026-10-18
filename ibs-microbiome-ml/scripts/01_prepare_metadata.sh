#!/usr/bin/env bash
set -euo pipefail

mkdir -p work metadata
curl -fsSL --retry 3 'https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/runinfo?acc=PRJNA637763' -o work/runinfo.csv

python3 - <<'PY'
import csv
import re
from pathlib import Path

with open("work/runinfo.csv", encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

keep = []
seen_runs = set()
seen_sample_ids = set()
ambiguous = []

for row in rows:
    run = row.get("Run", "").strip()
    sample = row.get("SampleName", "").strip()
    if not run or not sample or run in seen_runs:
        continue

    # Use sample-level fields only. Avoid study-level text that can mention IBS
    # while describing both patients and healthy controls.
    fields = {
        key: str(row.get(key, "") or "").strip()
        for key in ("SampleName", "Disease", "Affection_Status", "SampleType", "source")
    }
    sample_text = " ".join(fields.values()).upper()
    is_control = bool(
        re.search(r"\bHEALTHY\b|\bCONTROL(?:S)?\b|\bHC\b", sample_text)
    )
    is_ibs = bool(re.search(r"\bIBS\b|IRRITABLE\s+BOWEL", sample_text))

    if is_control and is_ibs:
        ambiguous.append((run, sample, sample_text))
        continue
    if is_control:
        label = "HC"
        label_source = next(
            (key for key, value in fields.items()
             if re.search(r"\bHEALTHY\b|\bCONTROL(?:S)?\b|\bHC\b", value.upper())),
            "sample-level metadata",
        )
    elif is_ibs:
        label = "IBS"
        label_source = next(
            (key for key, value in fields.items()
             if re.search(r"\bIBS\b|IRRITABLE\s+BOWEL", value.upper())),
            "sample-level metadata",
        )
    else:
        continue

    sample_id = re.sub(r"[^A-Za-z0-9_.-]", "_", sample)
    if sample_id in seen_sample_ids:
        raise SystemExit(
            f"Duplicate sample ID after normalization: {sample!r} -> {sample_id!r}"
        )
    seen_runs.add(run)
    seen_sample_ids.add(sample_id)
    keep.append(
        (sample_id, run, label, row.get("BioSample", ""), row.get("Experiment", ""), label_source)
    )

labels = {item[2] for item in keep}
if len(keep) < 100 or labels != {"IBS", "HC"}:
    raise SystemExit(
        f"Unexpected metadata extraction: {len(keep)} rows; labels={sorted(labels)}"
    )
if ambiguous:
    preview = "; ".join(f"{run} ({sample})" for run, sample, _ in ambiguous[:10])
    raise SystemExit(f"Ambiguous sample labels need manual review: {preview}")

with open("metadata/sample-metadata.tsv", "w", encoding="utf-8", newline="") as handle:
    handle.write("sample-id\tsra_accession\tgroup\tbiosample\texperiment\tlabel_source\n")
    for sample_id, run, label, biosample, experiment, label_source in keep:
        handle.write(
            f"{sample_id}\t{run}\t{label}\t{biosample}\t{experiment}\t{label_source}\n"
        )

counts = {label: sum(item[2] == label for item in keep) for label in ("IBS", "HC")}
print(f"Wrote {len(keep)} samples; IBS={counts['IBS']}, HC={counts['HC']}")
PY
