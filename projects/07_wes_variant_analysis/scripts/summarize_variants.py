#!/usr/bin/env python3
"""Create a lightweight variant summary from a VCF."""

import csv
import sys

vcf_path = sys.argv[1]
output_path = sys.argv[2]

total = 0
passing = 0

with open(vcf_path, encoding="utf-8") as handle:
    for line in handle:
        if line.startswith("#"):
            continue
        fields = line.rstrip("\n").split("\t")
        if len(fields) < 7:
            continue
        total += 1
        if fields[6] == "PASS":
            passing += 1

with open(output_path, "w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["metric", "value"])
    writer.writerow(["variants_total", total])
    writer.writerow(["variants_pass", passing])
