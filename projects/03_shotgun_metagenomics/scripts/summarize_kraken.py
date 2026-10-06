from pathlib import Path
import sys

report, top_out, report_md, metadata = map(Path, sys.argv[1:])
rows = []
root_pct = None
root_count = None
unclassified = None
for line in report.read_text().splitlines():
    p = line.split("\t")
    if len(p) < 6:
        continue
    rank = p[3].strip()
    if rank == "S":
        rows.append((float(p[0]), p[5].strip(), p[4].strip()))
    elif rank == "R":
        root_pct, root_count = float(p[0]), int(p[1])
    elif rank == "U":
        unclassified = int(p[1])
rows.sort(key=lambda x: x[0], reverse=True)
with top_out.open("w") as f:
    f.write("percent_total_fragments\\ttaxon\\ttaxid\\n".replace("\\\\", "\\"))
    for pct, name, taxid in rows[:15]:
        f.write(f"{pct:.2f}\\t{name}\\t{taxid}\\n".replace("\\\\", "\\"))
meta = dict(line.split("\\t", 1) for line in metadata.read_text().splitlines() if "\\t" in line)
lines = ["# Actual outcome — shotgun metagenomics", "", "Public-data-only paired-end WGS analysis.", "", "## Provenance"]
for label, key in [("Run", "run_accession"), ("BioProject", "project_accession"), ("BioSample", "sample_accession"), ("Experiment", "experiment_accession"), ("Study", "study_accession"), ("Platform", "instrument_platform"), ("Strategy", "library_strategy"), ("Layout", "library_layout")]:
    lines.append(f"- {label}: {meta.get(key, 'not recorded')}")
lines += ["", "## Kraken2", "- Database: Standard-8 June 2026"]
if root_pct is not None:
    lines.append(f"- Classified: {root_count:,} fragments ({root_pct:.2f}%)")
if unclassified is not None:
    lines.append(f"- Unclassified: {unclassified:,} fragments")
lines += ["", "## Top species", f"- Leading species: {rows[0][1]} ({rows[0][0]:.2f}% of total fragments)" if rows else "- No species reported", "- See top_taxa.tsv", "", "## Comparison", "- See CLASSIFIER_COMPARISON.md and classifier_comparison.tsv", "- Kraken2 percentages and Centrifuge abundance estimates are not directly interchangeable.", "", "## Interpretation", "One public sample cannot establish NEC-associated taxa, biomarkers, causality, prevalence, or cohort-level differences."]
report_md.write_text("\\n".join(lines).replace("\\n", "\n") + "\n")
