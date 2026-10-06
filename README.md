# Bioinformatics Portfolio

A practical, reproducible bioinformatics portfolio built around **public biological datasets**.

## Portfolio roadmap

| # | Project | Main skills | Status |
|---|---|---|---|
| 01 | [16S Microbiome Analysis](projects/01_16s_microbiome/) | NCBI SRA, FASTQ, FastQC, MultiQC, nf-core/ampliseq, QIIME 2 | 🟢 Completed |
| 02 | [IBS Microbiome Analysis](projects/02_ibs_microbiome/) | 16S, QIIME 2, Deblur, SILVA, diversity, machine learning | 🟢 Completed |
| 03 | [Shotgun Metagenomics](projects/03_shotgun_metagenomics/) | FASTP, Kraken2, Centrifuge, taxonomic profiling | 🟢 Completed |
| 04 | [Nextflow / nf-core Pipeline](projects/04_nfcore_pipeline/) | workflow engineering, containers, reproducibility, CI | 🟢 Completed |
| 05 | Bioinformatics + Machine Learning | Python, feature engineering, model evaluation | Planned |
| 06 | RNA-seq / Transcriptomics | QC, alignment/quantification, differential expression | Planned |

> Projects are added one at a time. The repository will not contain fabricated results: generated results are added only after the corresponding workflow has actually been run.

---

## Project 01 — Public 16S Gut Microbiome Analysis

End-to-end 16S rRNA amplicon workflow using a public NCBI SRA human stool run.

**Dataset:** SRR26534086 • BioSample SAMN37943185 • BioProject PRJNA1031545 • Illumina MiSeq • paired-end • V3–V4.

**Workflow:** NCBI SRA → download → validation → FASTQ → FastQC/MultiQC → paired-read validation → nf-core/ampliseq + Docker → QIIME 2/SILVA → downstream analysis.

**Key points**
- Public-data-only workflow with accession-level provenance.
- Raw FASTQ/SRA files and intermediate artifacts remain outside Git.
- One sample is used for workflow learning and validation, not cohort-level inference.
- Detailed execution, provenance, troubleshooting and interpretation are documented in the project README.

[Open Project 01 →](projects/01_16s_microbiome/)

---

## Project 02 — IBS Microbiome Classification

Public-data-only cohort analysis using **PRJNA637763**, containing **85 IBS samples and 26 healthy controls**.

**Analysis**
- 16S V1–V2, Illumina MiSeq paired-end
- QIIME 2 Deblur on forward reads
- SILVA 138 99% taxonomy
- Genus-level feature engineering
- Leakage-safe scikit-learn logistic regression and random forest
- Stratified 5-fold cross-validation

**Verified results**
- 111 samples total
- 131 genus-level features after prevalence filtering
- Mean observed features: IBS 275.38; healthy controls 301.96
- Mean Shannon diversity: IBS 3.9586; healthy controls 4.2491
- Logistic regression ROC-AUC: **0.9186**
- Random forest ROC-AUC: **0.8604**
- Logistic regression accuracy: **0.8288**
- Random forest accuracy: **0.7748**

These are results from an independent public-data re-analysis, not a claim of reproducing the original paper's private preprocessing or model.

[Open Project 02 →](projects/02_ibs_microbiome/)

---

## Project 03 — Public Shotgun Metagenomics

End-to-end shotgun metagenomics taxonomic profiling using a real public human infant fecal WGS sample.

**Dataset:** PRJNA273761 • SRR1779146 • SAMN03295851 • SRX858749 • Illumina HiSeq 2000 • WGS • paired-end.

**Workflow**

NCBI/ENA WGS → FASTP QC → Kraken2 → Centrifuge → independent classifier comparison → top-taxa/QC/provenance reports.

**Verified results**
- Kraken2 classified **6,940,503 / 7,954,717 fragments (87.25%)**
- Leading Kraken2 species: **Enterobacter roggenkampii (17.06%)**
- Top-10 classifier species overlap: **7/10**
- Top-10 Jaccard similarity: **0.5385**
- GitHub Actions run #15 completed successfully with both classifiers.

**Interpretation boundary:** this is a single-run taxonomic profile. It does not establish NEC-associated taxa, biomarkers, causality, prevalence or cohort-level differences.

[Open Project 03 →](projects/03_shotgun_metagenomics/)

---

## Project 04 — Production-style Nextflow / nf-core

Project 04 moves from individual analysis scripts to **workflow engineering**. It validates nf-core/rnaseq 3.27.0 using the public nf-core test profile, Docker containers and GitHub Actions CI.

The project is **completed**: GitHub Actions run #2 succeeded and the generated CI artifact was verified.

[Open Project 04 →](projects/04_nfcore_pipeline/)

---

## Reproducibility principles

- Use public accession numbers whenever possible.
- Record exact datasets and metadata before analysis.
- Keep raw data outside Git.
- Validate downloads before analysis.
- Run QC before choosing trimming parameters.
- Record software versions and resource limits.
- Keep pipeline parameters separate from scripts.
- Do not report biological conclusions from a single sample as cohort-level findings.
- Separate observed results from interpretation.

## Author

**Ashoka B**  
Bioinformatics • Computational Biology • Data Analysis • Machine Learning
