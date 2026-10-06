# Bioinformatics Portfolio

A practical bioinformatics portfolio focused on **genomics, microbiome analysis, metagenomics, transcriptomics, and machine learning** using public biological datasets.

The projects are designed to demonstrate real-world analysis skills, reproducible workflows, biological interpretation, and data-driven problem solving.

## Projects

| # | Project | Focus | Status |
|---|---|---|---|
| 01 | [16S Microbiome Analysis](projects/01_16s_microbiome/) | 16S rRNA, QIIME 2, SRA, microbiome profiling | 🟢 Completed |
| 02 | [IBS Microbiome Analysis](projects/02_ibs_microbiome/) | 16S, diversity analysis, machine learning | 🟢 Completed |
| 03 | [Shotgun Metagenomics](projects/03_shotgun_metagenomics/) | WGS, Kraken2, Centrifuge, taxonomic profiling | 🟢 Completed |
| 04 | [Nextflow / nf-core Pipeline](projects/04_nfcore_pipeline/) | Nextflow, nf-core, Docker, workflow engineering | 🟢 Completed |
| 05 | [Bioinformatics + Machine Learning](projects/05_bioinformatics_ml/) | Transcriptomics, feature selection, scikit-learn | 🟢 Completed |
| 06 | RNA-seq / Transcriptomics | QC, quantification, differential expression | Planned |

---

## Project 01 — 16S Gut Microbiome Analysis

End-to-end 16S rRNA amplicon analysis using a public human stool sample from NCBI SRA.

**Dataset:** SRR26534086 • BioSample SAMN37943185 • BioProject PRJNA1031545 • Illumina MiSeq • paired-end • V3–V4.

**Workflow:** SRA → FASTQ validation → FastQC/MultiQC → nf-core/ampliseq → QIIME 2 → SILVA taxonomy → downstream analysis.

The project documents the complete workflow, software configuration, provenance, troubleshooting and interpretation.

[Open Project 01 →](projects/01_16s_microbiome/)

---

## Project 02 — IBS Microbiome Classification

A public cohort analysis using **PRJNA637763**, containing **85 IBS samples and 26 healthy controls**.

**Analysis**
- 16S V1–V2 Illumina MiSeq data
- QIIME 2 Deblur
- SILVA 138 99% taxonomy
- Genus-level feature engineering
- Diversity analysis
- Logistic Regression and Random Forest
- Stratified 5-fold cross-validation

**Results**
- 111 samples
- 131 genus-level features after prevalence filtering
- Mean Shannon diversity: IBS **3.9586**; healthy controls **4.2491**
- Logistic Regression ROC-AUC: **0.9186**
- Random Forest ROC-AUC: **0.8604**

[Open Project 02 →](projects/02_ibs_microbiome/)

---

## Project 03 — Shotgun Metagenomics

Shotgun metagenomic taxonomic profiling of a real public human infant fecal WGS sample.

**Dataset:** PRJNA273761 • SRR1779146 • SAMN03295851 • SRX858749 • Illumina HiSeq 2000 • paired-end WGS.

**Workflow**

WGS reads → FASTP → Kraken2 → Centrifuge → classifier comparison → taxonomic profiling and QC.

**Results**
- 7,954,717 fragments analyzed
- Kraken2 classified **87.25%** of fragments
- Leading Kraken2 species: **Enterobacter roggenkampii (17.06%)**
- Top-10 classifier overlap: **7/10**
- Top-10 Jaccard similarity: **0.5385**

This project deliberately treats the sample as a single-run analysis and does not make cohort-level NEC, biomarker or causality claims.

[Open Project 03 →](projects/03_shotgun_metagenomics/)

---

## Project 04 — Nextflow / nf-core Workflow Engineering

A production-style workflow engineering project built around **nf-core/rnaseq 3.27.0**.

The project demonstrates:

- Nextflow workflow execution
- nf-core pipeline usage
- Docker-based reproducibility
- Parameterized execution
- Test-data validation
- Structured workflow outputs

The focus is on building and validating a reproducible computational workflow rather than making biological claims from the test dataset.

[Open Project 04 →](projects/04_nfcore_pipeline/)

---

## Project 05 — Bioinformatics + Machine Learning

Machine-learning analysis of public breast cancer transcriptomics data from **NCBI GEO GSE42568**.

**Dataset**
- 121 samples
- 104 breast cancer
- 17 normal breast tissue
- Affymetrix GPL570
- 54,579 non-constant probes

**Approach**
- Expression-matrix processing
- Variance filtering
- Leakage-safe feature selection
- Logistic Regression
- Random Forest
- Stratified 5-fold cross-validation
- ROC-AUC and average-precision evaluation
- Exploratory feature ranking

**Results**

| Model | ROC-AUC | Average Precision |
|---|---:|---:|
| Logistic Regression | **0.9802** | **0.9964** |
| Random Forest | **0.9740** | **0.9953** |

The results demonstrate classification performance within this public dataset. They are not presented as clinical diagnostic validation or independently validated biomarkers.

[Open Project 05 →](projects/05_bioinformatics_ml/)

---

## Reproducibility

The portfolio follows a consistent approach:

- Public datasets and accession numbers are recorded.
- Raw data and large intermediate files are kept outside the repository.
- Software versions and important parameters are documented.
- Quality control is performed before downstream analysis.
- Results are reported only after the corresponding analysis has been executed.
- Single-sample analyses are not presented as cohort-level findings.
- Observed results are separated from biological interpretation.

## Skills Demonstrated

**Bioinformatics:**  
16S rRNA analysis • microbiome analysis • metagenomics • transcriptomics • NGS workflows • taxonomic profiling

**Tools:**  
QIIME 2 • nf-core • Nextflow • Kraken2 • Centrifuge • FASTP • FastQC • MultiQC • SILVA

**Programming & Data:**  
Python • R • SQL • Linux • Bash • Pandas • NumPy • scikit-learn • data visualization

**Workflow & Analysis:**  
Machine learning • feature engineering • statistical analysis • workflow automation • reproducible research

## Author

**Ashoka B**

Bioinformatics • Computational Biology • Data Analysis • Machine Learning
