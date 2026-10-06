# 03 — Public Shotgun Metagenomics Taxonomic Profiling

End-to-end shotgun metagenomics workflow using a public NCBI human gut metagenome.

## Dataset

- BioProject: PRJNA786061
- Study: Association between anemia and gut microbiome composition in the rural Odisha population
- Data type: human gut metagenome
- Source cohort: 102 SRA experiments, approximately 3.1 GB
- Analysis scope: one paired-end shotgun run selected automatically from the public ENA run API

## Workflow

```text
NCBI/ENA public run → FASTQ → FASTP → Kraken 2 → taxonomic report → top-taxa summary
```

Kraken 2 classifies DNA reads using k-mer/minimizer matches and a lowest-common-ancestor framework. It supports paired-end classification.

## Reference database

MiniKraken2 v2 8-GB: RefSeq bacteria, archaea and viruses plus the GRCh38 human genome. This reduced database is used deliberately because the full Kraken 2 standard database is too large for ordinary GitHub-hosted CI resources.

## Reproducibility

The workflow resolves a public run, records its accession metadata, downloads the FASTQ files, performs FASTP filtering, downloads the pinned MiniKraken2 database, runs Kraken 2, and commits only derived results. Raw FASTQ files and the database are never committed.

## Results

The workflow creates:

- REPORT.md
- run_metadata.tsv
- fastp_summary.json
- kraken2.report
- top_taxa.tsv

### Interpretation boundary

This is a single-run taxonomic profile. It cannot establish anemia-associated taxa, biomarkers, causality, prevalence or cohort-level conclusions. A cohort analysis would require all 102 samples, consistent metadata, compositional analysis and statistical testing.

## Local execution

```bash
bash scripts/run_shotgun.sh
```

## Repository structure

```text
03_shotgun_metagenomics/
├── README.md
├── metadata/DATASET.md
├── scripts/run_shotgun.sh
├── scripts/summarize_kraken.py
└── results/
```
