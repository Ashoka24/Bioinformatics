#!/usr/bin/env python3
"""Build compact tables, figures, and a report from exported QIIME 2 results."""
import csv
import html
import math
from pathlib import Path

ROOT = Path("results_actual")


def read_tsv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.reader(handle, delimiter="\t"))


feature_rows = read_tsv(ROOT / "tables/feature-table.tsv")
taxonomy_rows = read_tsv(ROOT / "tables/taxonomy.tsv")

counts = {
    row[0]: int(float(row[1]))
    for row in feature_rows[1:]
    if len(row) > 1 and row[0] and not row[0].startswith("#")
}
taxonomy = {row[0]: row[1] for row in taxonomy_rows[1:] if len(row) > 1}

total_reads = sum(counts.values())
observed_features = len(counts)
if total_reads <= 0 or observed_features == 0:
    raise SystemExit("The exported feature table is empty; refusing to write a results report.")

proportions = [count / total_reads for count in counts.values() if count > 0]
shannon_natural_log = -sum(p * math.log(p) for p in proportions)
simpson = 1 - sum(p * p for p in proportions)
inverse_simpson = 1 / sum(p * p for p in proportions)
pielou_evenness = shannon_natural_log / math.log(observed_features) if observed_features > 1 else 0.0


def alpha_value(metric):
    path = ROOT / "tables" / metric / "alpha-diversity.tsv"
    if not path.exists():
        return "not available"
    rows = read_tsv(path)
    return rows[1][1] if len(rows) > 1 and len(rows[1]) > 1 else "not available"


# QIIME taxonomy strings use domain at index 0, phylum at index 1, etc.
taxonomic_levels = {
    1: "phylum",
    2: "class",
    3: "order",
    4: "family",
    5: "genus",
    6: "species",
}
for index, level_name in taxonomic_levels.items():
    abundance = {}
    for feature_id, count in counts.items():
        lineage = [part.strip() for part in taxonomy.get(feature_id, "Unclassified").split(";")]
        taxon = lineage[index] if len(lineage) > index and lineage[index] else "Unclassified"
        abundance[taxon] = abundance.get(taxon, 0) + count

    output = ROOT / "tables" / f"{level_name}_abundance.tsv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["taxon", "read_count", "relative_abundance_percent"])
        for taxon, count in sorted(abundance.items(), key=lambda item: item[1], reverse=True):
            writer.writerow([taxon, count, f"{100 * count / total_reads:.4f}"])


def write_abundance_figure(level_name, title):
    table_path = ROOT / "tables" / f"{level_name}_abundance.tsv"
    with table_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))[:15]

    values = [(row["taxon"], float(row["relative_abundance_percent"])) for row in rows]
    maximum = max((value for _, value in values), default=1.0) or 1.0
    height = 80 + 32 * len(values)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}">',
        f'<text x="20" y="30" font-size="20">{html.escape(title)}</text>',
    ]
    y = 55
    for taxon, value in values:
        width = 480 * value / maximum
        svg.extend([
            f'<text x="20" y="{y + 15}" font-size="12">{html.escape(taxon[:70])}</text>',
            f'<rect x="450" y="{y}" width="{width:.1f}" height="20" fill="currentColor"/>',
            f'<text x="950" y="{y + 15}" font-size="12">{value:.2f}%</text>',
        ])
        y += 32
    svg.append("</svg>")
    figure_dir = ROOT / "figures"
    figure_dir.mkdir(exist_ok=True)
    (figure_dir / f"{level_name}_relative_abundance.svg").write_text(
        "\n".join(svg) + "\n", encoding="utf-8"
    )


write_abundance_figure("phylum", "SRR26534086 — relative abundance by phylum")
write_abundance_figure("genus", "SRR26534086 — relative abundance by genus")

report = [
    "# Actual outcome — SRR26534086",
    "",
    "Results generated from one public NCBI SRA run. This is a workflow demonstration, not a cohort-level or clinical analysis.",
    "",
    "## Dataset",
    "- BioSample: `SAMN37943185`",
    "- BioProject: `PRJNA1031545`",
    "- Experiment: `SRX22237515`",
    "- Assay: 16S rRNA V3–V4 amplicon",
    "- Instrument: Illumina MiSeq",
    "",
    "## Processing",
    "- QIIME 2 amplicon Docker image: `2024.10`",
    "- Primer trimming with QIIME 2 Cutadapt using the documented V3–V4 primers",
    "- Denoising: QIIME 2 Deblur `denoise-16S`, trim length 200 bp",
    "- Taxonomy: SILVA 138 99% Naive Bayes classifier",
    "- Classifier SHA-256: `c08a1aa4d56b449b511f7215543a43249ae9c54b57491428a7e5548a62613616`",
    "",
    "This result was produced by the Deblur workflow above. It should not be described as a DADA2 run or as using the separate nf-core/ampliseq truncation settings.",
    "",
    "## Results",
    f"- Reads represented in the exported feature table: **{total_reads:,}**",
    f"- Observed features: **{observed_features}**",
    f"- Shannon diversity (natural logarithm, calculated from feature counts): **{shannon_natural_log:.6f}**",
    f"- Simpson diversity (1 − sum of squared proportions): **{simpson:.6f}**",
    f"- Inverse Simpson diversity: **{inverse_simpson:.6f}**",
    f"- Pielou evenness: **{pielou_evenness:.6f}**",
    f"- QIIME 2 observed features: **{alpha_value('observed_features')}**",
    f"- QIIME 2 Shannon entropy (base 2): **{alpha_value('shannon')}**",
    "",
    "The two Shannon values use different logarithm bases: the value calculated here uses the natural logarithm, while the QIIME 2 output uses base 2. They describe the same feature-count distribution and should not be compared without accounting for that difference.",
    "",
    "## Taxonomy outputs",
    "Phylum-, class-, order-, family-, genus-, and species-level abundance tables were generated from the feature counts and assigned taxonomy. Taxonomic assignments remain dependent on the reference classifier and should be interpreted accordingly.",
    "",
    "Beta diversity and PERMANOVA are omitted because this analysis contains only one sample.",
    "",
]
(ROOT / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
