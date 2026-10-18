#!/usr/bin/env python3
"""Summarize a Kraken2 report and write the project results report."""
from pathlib import Path
import sys

report_path, top_out, report_md, metadata_path = map(Path, sys.argv[1:])
species = []
total_fragments = None
unclassified_fragments = None

for line in report_path.read_text(encoding="utf-8").splitlines():
    fields = line.split("\t")
    if len(fields) < 6:
        continue
    try:
        percentage = float(fields[0].strip())
        count = int(fields[1].strip())
    except ValueError:
        continue

    rank = fields[3].strip()
    if rank == "S":
        species.append((percentage, fields[5].strip(), fields[4].strip()))
    elif rank == "R":
        total_fragments = count
    elif rank == "U":
        unclassified_fragments = count

species.sort(key=lambda item: item[0], reverse=True)
with top_out.open("w", encoding="utf-8", newline="") as handle:
    handle.write("percent_total_fragments\ttaxon\ttaxid\n")
    for percentage, name, taxid in species[:15]:
        handle.write(f"{percentage:.2f}\t{name}\t{taxid}\n")

metadata = {
    key: value
    for line in metadata_path.read_text(encoding="utf-8").splitlines()
    if "\t" in line
    for key, value in [line.split("\t", 1)]
}
lines = [
    "# Actual outcome — shotgun metagenomics",
    "",
    "Public paired-end WGS analysis.",
    "",
    "## Provenance",
]
for label, key in [
    ("Run", "run_accession"),
    ("BioProject", "project_accession"),
    ("BioSample", "sample_accession"),
    ("Experiment", "experiment_accession"),
    ("Study", "study_accession"),
    ("Platform", "instrument_platform"),
    ("Strategy", "library_strategy"),
    ("Layout", "library_layout"),
]:
    lines.append(f"- {label}: {metadata.get(key, 'not recorded')}")

lines.extend(["", "## Kraken2", "- Database: Standard-8 June 2026"])
if total_fragments is not None and unclassified_fragments is not None and total_fragments > 0:
    classified = total_fragments - unclassified_fragments
    classified_pct = 100 * classified / total_fragments
    unclassified_pct = 100 * unclassified_fragments / total_fragments
    lines.extend([
        f"- Total fragments: **{total_fragments:,}**",
        f"- Classified: **{classified:,} ({classified_pct:.2f}%)**",
        f"- Unclassified: **{unclassified_fragments:,} ({unclassified_pct:.2f}%)**",
    ])
elif total_fragments is not None:
    lines.append(f"- Total fragments: **{total_fragments:,}**")
    lines.append("- Classified/unclassified counts could not be calculated from the report.")

if species:
    lines.append(f"- Leading species: **{species[0][1]}** ({species[0][0]:.2f}% of total fragments)")
else:
    lines.append("- No species-level assignments were reported.")

lines.extend([
    "- See top_taxa.tsv for the leading species-level assignments.",
    "",
    "## Comparison",
    "- See CLASSIFIER_COMPARISON.md and classifier_comparison.tsv.",
    "- Kraken2 percentages and Centrifuge abundance estimates are not directly interchangeable.",
    "",
    "## Interpretation",
    "This is one public infant fecal sample. It cannot establish NEC-associated taxa, biomarkers, causality, prevalence, or cohort-level differences.",
])
report_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
