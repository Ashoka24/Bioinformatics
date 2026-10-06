from pathlib import Path
import sys

report, top_out, report_md, metadata = map(Path, sys.argv[1:])

rows = []
for line in report.read_text().splitlines():
    p = line.split("\t")
    if len(p) < 8:
        continue
    try:
        pct = float(p[0])
    except ValueError:
        continue
    if p[3] == "S" and p[7].strip():
        rows.append((pct, p[7].strip(), p[2]))

rows.sort(reverse=True)

with top_out.open("w") as f:
    f.write("percent_classified_reads\ttaxon\ttaxid\n")
    for pct, name, taxid in rows[:15]:
        f.write(f"{pct:.6f}\t{name}\t{taxid}\n")

meta = {}
for line in metadata.read_text().splitlines():
    if "\t" in line:
        k, v = line.split("\t", 1)
        meta[k] = v

root_pct = None
for line in report.read_text().splitlines():
    p = line.split("\t")
    if len(p) >= 8 and p[3] == "R":
        try:
            root_pct = float(p[0])
        except ValueError:
            pass
        break

lines = [
    "# Actual outcome — shotgun metagenomics",
    "",
    "Public-data-only analysis of one paired-end shotgun-metagenomic run from PRJNA273761.",
    "",
    "## Run",
    f"- Run accession: {meta.get('RUN_ACCESSION','')}",
    f"- BioProject: {meta.get('STUDY_ACCESSION','')}",
    f"- BioSample: {meta.get('SAMPLE_ACCESSION','')}",
    f"- Experiment: {meta.get('EXPERIMENT_ACCESSION','')}",
    f"- Platform: {meta.get('INSTRUMENT_PLATFORM','')}",
    f"- Library strategy: {meta.get('LIBRARY_STRATEGY','')}",
    f"- Layout: {meta.get('LIBRARY_LAYOUT','')}",
    "",
    "## Kraken 2",
    "- Database: Kraken 2 Standard-8 archive (June 2026)",
]
if root_pct is not None:
    lines.append(f"- Root-level classified-read percentage: **{root_pct:.4f}%**")
lines += [
    "",
    "## Top species",
    "The 15 highest-abundance species reported by Kraken 2 are stored in top_taxa.tsv.",
    "",
    "## Interpretation",
    "This is a single-run taxonomic profile. It does not establish anemia-associated taxa, biomarkers, causality, prevalence or cohort-level conclusions.",
]
report_md.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
