# 16S rRNA Microbiome Analysis — Moving Pictures Case Study

A small, reproducible microbiome analysis built around the **QIIME 2 Moving Pictures** human microbiome dataset. The goal is to demonstrate the reasoning and downstream analysis that follows an amplicon workflow, rather than simply listing tools.

> **Data provenance:** The five-ASV feature-table excerpt is taken from the public `qiime2R` Moving Pictures example, and the corresponding sample metadata comes from public QIIME 2 tutorial/test data. This repository does **not** contain private or clinical data.

## Biological question

Can a small set of bacterial sequence variants show differences in community structure and alpha diversity across longitudinal gut samples?

This is a **portfolio-scale demonstration**, not a statistically powered biological study. The five-ASV subset is deliberately small so that every calculation can be inspected.

## Dataset

The underlying Moving Pictures tutorial contains human microbiome samples collected from two individuals across multiple body sites and time points. The original data used an Illumina HiSeq 16S rRNA V4 protocol. The full tutorial performs demultiplexing, DADA2 denoising, taxonomy assignment, diversity analysis, and differential-abundance analysis.

This repository uses a small published excerpt for transparent downstream analysis.

- QIIME 2 Moving Pictures tutorial: https://amplicon-docs.qiime2.org/en/latest/tutorials/moving-pictures/
- qiime2R example and data description: https://github.com/jbisanz/qiime2R
- Original study: Caporaso et al. (2011), *Moving Pictures of the Human Microbiome*

## Workflow

```text
Public 16S dataset
       │
       ▼
Feature table + sample metadata
       │
       ├── Read-depth / feature-count QC
       ├── Relative-abundance transformation
       ├── Shannon alpha diversity
       ├── Bray–Curtis distance
       └── PCoA ordination
               │
               ▼
        Biological interpretation
```

## Repository structure

```text
.
├── data/
│   ├── feature-table.tsv
│   └── sample-metadata.tsv
├── figures/
│   ├── bray_curtis_pcoa.svg
│   ├── relative_abundance_heatmap.svg
│   └── shannon_diversity.svg
├── results/
│   ├── bray_curtis_pcoa.csv
│   ├── sample_summary.csv
│   └── top_features.csv
├── scripts/
│   └── analyze_microbiome.py
├── requirements.txt
└── README.md
```

## Reproduce the analysis

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/analyze_microbiome.py
```

The analysis produces sample-level read depth, observed feature counts, Shannon diversity, mean relative abundance, and Bray–Curtis PCoA coordinates.

## What I looked for

### 1. Sequencing depth

Total feature counts are inspected before comparing samples. Unequal sequencing depth can influence naive abundance comparisons.

### 2. Alpha diversity

Shannon diversity captures both richness and evenness:

```text
H' = -Σ(pᵢ × ln(pᵢ))
```

where (p_i) is the relative abundance of feature (i).

### 3. Community structure

Bray–Curtis dissimilarity is calculated from relative abundances and visualized with PCoA. Samples that are closer in the ordination have more similar community composition under this distance measure.

### 4. Biological interpretation

The five-ASV subset is useful for demonstrating analysis mechanics, but it is **not sufficient to make a clinical or population-level microbiome claim**.

## Results from the reproducible run

| Sample | Reads in subset | Observed ASVs | Shannon |
|---|---:|---:|---:|
| L1S105 | 2,990 | 3 | 0.593 |
| L1S140 | 3,423 | 2 | 0.643 |
| L1S208 | 2,811 | 2 | 0.559 |
| L1S257 | 1,597 | 2 | 0.567 |
| L1S281 | 1,979 | 2 | 0.371 |

The dominant feature in this excerpt accounts for approximately 60.7% of the mean relative abundance across the five samples.

These values describe **this small excerpt only**; they should not be interpreted as the diversity of the complete microbiome dataset.

## Next experimental extension

The next version of this case study should use the complete Moving Pictures feature table and taxonomy and reproduce:

1. QIIME 2 import and DADA2 denoising
2. Taxonomic classification
3. Alpha/beta diversity
4. Taxa bar plots
5. Gut-only filtering
6. Differential abundance with ANCOM-BC
7. Comparison of subjects and longitudinal time points
8. Reproducible environment/containerization

That full analysis will be kept separate from this deliberately small, inspectable example.
