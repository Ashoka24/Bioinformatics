# Bioinformatics Portfolio

A practical, reproducible bioinformatics portfolio built around **public biological datasets**.

The repository is organized as independent projects. Each project is written so that another reader can understand:

**biological question → public data → file organization → quality control → analysis → results → interpretation → limitations**

## Portfolio roadmap

| # | Project | Main skills | Status |
|---|---|---|---|
| 01 | [16S Microbiome Analysis](projects/01_16s_microbiome/) | NCBI SRA, FASTQ, FastQC, MultiQC, nf-core/ampliseq, QIIME 2 | 🟢 Completed |
| 02 | [IBS Microbiome Analysis](projects/02_ibs_microbiome/) | 16S microbiome analysis, QIIME 2, Deblur, SILVA, alpha diversity, machine learning | 🟢 Completed |
| 03 | [Shotgun Metagenomics](projects/03_shotgun_metagenomics/) | FASTP, Kraken2, Centrifuge, taxonomic profiling and classifier comparison | 🟢 Completed |
| 04 | Nextflow / nf-core Pipeline | workflow engineering, containers, reproducibility | Planned |
| 05 | Bioinformatics + Machine Learning | Python, feature engineering, model evaluation | Planned |
| 06 | RNA-seq / Transcriptomics | QC, alignment/quantification, differential expression | Planned |

> Projects will be added one at a time. The repository will not contain fabricated results: generated results are added only after the corresponding workflow has actually been run.

## Project design

Every project follows the same structure:

```text
project/
├── README.md
├── docs/
├── metadata/
├── params/
├── scripts/
└── logs/
```

Large sequencing files, credentials, temporary pipeline work directories, and generated QIIME 2 artifacts are intentionally kept out of Git.

## Local data convention

The examples use a local Windows data folder:

```text
C:\Users\ashok\OneDrive\Desktop\Ashoka\data
```

When running the Bash scripts from WSL, the same folder is:

```text
/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data
```

You can override the path in every script with `DATA_ROOT`.

## Start here

Go to **[Project 01 — 16S Microbiome Analysis](projects/01_16s_microbiome/)**.

The first project uses a public NCBI SRA human stool 16S dataset rather than private/company data. The selected run is `SRR26534086`, linked to BioProject `PRJNA1031545`. NCBI describes it as paired-end Illumina MiSeq 16S V3–V4 amplicon data and provides the primer sequences used for the experiment.

### Project 02 — IBS Microbiome Analysis

The second project is a public-data re-analysis of BioProject `PRJNA637763`.

**Verified cohort results:**
- **111 samples** analyzed
- **85 IBS** samples
- **26 healthy controls**
- **131 genus-level features** after prevalence filtering
- Mean observed features: **275.38 IBS vs 301.96 HC**
- Mean Shannon diversity: **3.9586 IBS vs 4.2491 HC**
- L1 Logistic Regression: **ROC-AUC 0.9186**
- Random Forest: **ROC-AUC 0.8604**
- Machine-learning evaluation: **5-fold stratified cross-validation**

These are independent re-analysis metrics and are **not clinical diagnostic-validation results**.

See the complete [Project 02 documentation and verified results](projects/02_ibs_microbiome/).

## Reproducibility principles

- Use public accession numbers whenever possible.
- Record the exact dataset and metadata before analysis.
- Keep raw data outside Git.
- Validate downloads before analysis.
- Run QC before choosing trimming parameters.
- Record software versions and resource limits.
- Keep pipeline parameters in a separate file.
- Do not report biological conclusions from a single sample as if they were cohort-level findings.
- Separate observed results from interpretation.

## Author

**Ashoka B**  
Bioinformatics • Computational Biology • Data Analysis • Machine Learning
