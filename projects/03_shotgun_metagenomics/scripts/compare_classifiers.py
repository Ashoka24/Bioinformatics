#!/usr/bin/env python3
import csv, sys
from collections import OrderedDict

kraken_report, centrifuge_report, out = sys.argv[1:]

# Kraken report: percent, clade reads, direct reads, rank, taxid, name.
kraken = {}
with open(kraken_report, newline="") as f:
    for row in csv.reader(f, delimiter="\t"):
        if len(row) < 6:
            continue
        rank = row[3].strip()
        name = row[5].strip()
        if rank == "S":
            try:
                kraken[name] = float(row[0].strip())
            except ValueError:
                pass

centrifuge = {}
with open(centrifuge_report, newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        rank = row.get("taxRank", "")
        name = row.get("name", "").strip()
        if rank == "species" or rank == "leaf":
            try:
                abundance = float(row.get("abundance", "0"))
            except ValueError:
                abundance = 0.0
            centrifuge[name] = abundance * 100.0

top_k = [x[0] for x in sorted(kraken.items(), key=lambda x: x[1], reverse=True)[:10]]
top_c = [x[0] for x in sorted(centrifuge.items(), key=lambda x: x[1], reverse=True)[:10]]
overlap = len(set(top_k) & set(top_c))
union = len(set(top_k) | set(top_c))
jaccard = overlap / union if union else 0.0

names = OrderedDict()
for name in top_k + top_c:
    names[name] = None

with open(out, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["taxon", "kraken2_percent", "centrifuge_abundance_percent"])
    for name in names:
        w.writerow([name, f"{kraken.get(name, 0.0):.6f}", f"{centrifuge.get(name, 0.0):.6f}"])

summary = out.replace("classifier_comparison.tsv", "CLASSIFIER_COMPARISON.md")
with open(summary, "w") as f:
    f.write("# Kraken2 vs Centrifuge comparison\n\n")
    f.write("The two classifiers were run on the same fastp-cleaned paired-end reads. ")
    f.write("Their abundance metrics are not assumed to be directly equivalent because the classifiers use different assignment and abundance procedures.\n\n")
    f.write(f"- Top-10 species overlap: {overlap}/10\n")
    f.write(f"- Top-10 species Jaccard overlap: {jaccard:.4f}\n")
    f.write("\nThe TSV contains the top-10 union and the classifier-specific reported metrics.\n")
