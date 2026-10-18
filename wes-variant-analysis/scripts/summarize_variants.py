#!/usr/bin/env python3
"""Create a lightweight variant summary from a plain-text or gzipped VCF."""
import csv
import gzip
import sys
from pathlib import Path

vcf_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
opener = gzip.open if vcf_path.suffix == ".gz" else open

total = 0
passing = 0
with opener(vcf_path, "rt", encoding="utf-8") as handle:
    for line in handle:
        if line.startswith("#"):
            continue
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 7:
            continue
        total += 1
        if fields[6] == "PASS":
            passing += 1

output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["metric", "value"])
    writer.writerow(["variants_total", total])
    writer.writerow(["variants_pass", passing])
