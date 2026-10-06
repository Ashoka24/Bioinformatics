from pathlib import Path
import sys

report, top_out, report_md, metadata = map(Path, sys.argv[1:])
rows = []
root_pct = root_count = unclassified = None
for line in report.read_text().splitlines():
    parts = line.split(chr(9))
    if len(parts) < 6:
        continue
    rank = parts[3].strip()
    if rank == "S":
        rows.append((float(parts[0]), parts[5].strip(), parts[4].strip()))
    elif rank == "R":
        root_pct, root_count = float(parts[0]), int(parts[1])
    elif rank == "U":
        unclassified = int(parts[1])
rows.sort(key=lambda item: item[0], reverse=True)
with top_out.open("w") as output:
    output.write(chr(9).join(["percent_total_fragments", "taxon", "taxid"]) + chr(10))
    for pct, name, taxid in rows[:15]:
        output.write(chr(9).join([f"{pct:.2f}", name, taxid]) + chr(10))
meta = dict(line.split(chr(9), 1) for line in metadata.read_text().splitlines() if chr(9) in line)
lines = ["# Actual outcome — shotgun metagenomics", "", "Public paired-end WGS analysis.", "", "## Provenance"]
for label, key in [("Run", "run_accession"), ("BioProject", "project_accession"), ("BioSample", "sample_accession"), ("Experiment", "experiment_accession"), ("Study", "study_accession"), ("Platform", "instrument_platform"), ("Strategy", "library_strategy"), ("Layout", "library_layout")]:
    lines.append(f"- {label}: {meta.get(key, 'not recorded')}")
lines.extend(["", "## Kraken2", "- Database: Standard-8 June 2026"])
if root_pct is not None:
    lines.append(f"- Classified: {root_count:,} fragments ({root_pct:.2f}%)")
if unclassified is not None:
    lines.append(f"- Unclassified: {unclassified:,} fragments")
lines.extend(["", "## Top species", f"- Leading species: {rows[0][1]} ({rows[0][0]:.2f}% of total fragments)" if rows else "- No species reported", "- See top_taxa.tsv", "", "## Comparison", "- See CLASSIFIER_COMPARISON.md and classifier_comparison.tsv", "- Kraken2 percentages and Centrifuge abundance estimates are not directly interchangeable.", "", "## Interpretation", "One public sample cannot establish NEC-associated taxa, biomarkers, causality, prevalence, or cohort-level differences."])
report_md.write_text(chr(10).join(lines) + chr(10))
