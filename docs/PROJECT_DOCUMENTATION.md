# Bioinformatics Portfolio — Complete Project Documentation

This document provides the detailed technical record for Projects 01–06 in this repository.

It is intended as the detailed companion to the main portfolio README. The main README is intentionally concise; this document preserves the technical depth of the individual projects.

---

# Project 01 — Public 16S Gut Microbiome Analysis

## 1. Objective

Build and document an end-to-end 16S rRNA amplicon workflow using a real public human stool sample from NCBI SRA.

The project demonstrates:

- Public NCBI/SRA data retrieval
- FASTQ validation
- Read-quality assessment
- Paired-end amplicon processing
- QIIME 2 analysis
- SILVA taxonomic classification
- Reproducible nf-core/ampliseq execution
- Downstream microbiome analysis
- Explicit interpretation limits for single-sample data

## 2. Dataset

| Field | Value |
|---|---|
| SRA run | SRR26534086 |
| BioSample | SAMN37943185 |
| BioProject | PRJNA1031545 |
| Experiment | SRX22237515 |
| Instrument | Illumina MiSeq |
| Layout | Paired-end |
| Target | 16S rRNA |
| Region | V3–V4 |
| Forward primer | CCTACGGGNGGCWGCAG |
| Reverse primer | GACTACHVGGGTATCTAATCC |
| Spots | 49,964 |
| Bases | ~22.5M |
| Download size | ~13.1 MB |

The parent study contains stool 16S data from 77 STEMI patients. This repository uses one public run for workflow development and validation and does not treat the single run as a cohort-level analysis.

## 3. Computational workflow

```text
NCBI SRA
  ↓
SRA download
  ↓
vdb-validate
  ↓
FASTQ extraction / validation
  ↓
FastQC
  ↓
MultiQC
  ↓
Paired-read validation
  ↓
nf-core/ampliseq
  ↓
QIIME 2
  ↓
Denoising / feature generation
  ↓
SILVA taxonomy
  ↓
Downstream diversity and taxonomic analysis
```

## 4. Main tools

- SRA Toolkit
- FastQC
- MultiQC
- Nextflow
- Docker
- nf-core/ampliseq
- QIIME 2
- DADA2/QIIME 2 components
- SILVA reference database

The repository documents the workflow configuration and provenance separately from the biological interpretation.

## 5. Analysis parameters

The documented V3–V4 workflow preserves:

- Forward primer: CCTACGGGNGGCWGCAG
- Reverse primer: GACTACHVGGGTATCTAATCC
- Truncation settings: 280 / 260
- SILVA-based taxonomy
- Docker execution
- nf-core/ampliseq 2.11.0

The repository's execution and troubleshooting documentation should be consulted before changing trimming parameters.

## 6. Local data handling

Example local data root:

`C:\Users\ashok\OneDrive\Desktop\Ashoka\data`

WSL equivalent:

`/mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data`

Scripts use a configurable data root rather than company-specific storage.

## 7. Execution order

1. `scripts/00_setup.sh`
2. `scripts/01_download_ncbi.sh`
3. `scripts/02_qc.sh`
4. `scripts/03_validate.sh`
5. `scripts/04_prepare_input.sh`
6. `scripts/05_run_ampliseq.sh`
7. `scripts/05_qiime2_downstream.sh`
8. `scripts/06_expand_bioproject.sh`

## 8. Quality control

QC is performed before downstream interpretation.

The workflow includes:

- SRA validation
- FASTQ/read validation
- FastQC
- MultiQC
- paired-end consistency checks
- pipeline-level QC

## 9. Repository outputs

- Workflow documentation
- Dataset provenance
- Parameter configuration
- Shell scripts
- QC documentation
- Workflow and output-map figures
- Downstream analysis documentation

Large FASTQ files, SRA archives, QIIME 2 artifacts, Nextflow work directories and generated logs are not committed.

## 10. Interpretation

A single sample can demonstrate:

- sequencing-read quality
- feature generation
- taxonomy
- descriptive community structure
- diversity calculations

It cannot establish:

- differential abundance
- disease association
- group-level microbiome signatures
- prevalence
- causal relationships

---

# Project 02 — IBS Microbiome Classification

## 1. Objective

Perform an independent public-data analysis of gut microbiome profiles from IBS patients and healthy controls.

The project extends beyond a basic microbiome workflow by combining:

- 16S processing
- taxonomic profiling
- alpha-diversity analysis
- genus-level feature engineering
- supervised machine learning
- leakage-safe cross-validation
- model evaluation

## 2. Dataset

| Field | Value |
|---|---|
| BioProject | PRJNA637763 |
| Study | Usefulness of Machine Learning-Based Gut Microbiome Analysis for Identifying Patients with Irritable Bowels Syndrome |
| IBS samples | 85 |
| Healthy controls | 26 |
| Total | 111 |
| Sequencing | Illumina MiSeq |
| Layout | Paired-end |
| Amplicon region | V1–V2 |

This is an independent public-data re-analysis and is not presented as an exact reproduction of the original study's private preprocessing or model.

## 3. Workflow

```text
Public SRA / ENA reads
  ↓
16S read processing
  ↓
QIIME 2
  ↓
Deblur
  ↓
SILVA 138 99% taxonomy
  ↓
Feature table
  ↓
Prevalence filtering
  ↓
Genus-level feature matrix
  ↓
Diversity analysis
  ↓
Machine learning
  ↓
Stratified 5-fold cross-validation
  ↓
Performance evaluation
```

## 4. Microbiome processing

The analysis uses:

- QIIME 2
- Deblur on forward reads
- SILVA 138 99% classifier
- genus-level abundance features
- prevalence filtering before machine-learning analysis

## 5. Cohort composition

- IBS: 85
- Healthy control: 26
- Total: 111

After prevalence filtering:

- 131 genus-level features

## 6. Diversity results

Mean observed features:

| Group | Mean observed features |
|---|---:|
| IBS | 275.38 |
| Healthy control | 301.96 |

Mean Shannon diversity:

| Group | Mean Shannon |
|---|---:|
| IBS | 3.9586 |
| Healthy control | 4.2491 |

These are descriptive cohort results from this public dataset.

## 7. Machine-learning models

### Logistic Regression

Evaluation used stratified 5-fold cross-validation.

Verified performance:

- ROC-AUC: 0.9186
- Accuracy: 0.8288
- Precision: 0.9342
- Sensitivity: 0.8353

### Random Forest

Verified performance:

- ROC-AUC: 0.8604
- Accuracy: 0.7748
- Precision: 0.7830
- Sensitivity: 0.9765

## 8. Why cross-validation matters

The classifier is evaluated with stratified folds so that IBS and healthy-control representation is preserved across training and evaluation splits.

The purpose is to estimate classification performance without evaluating the model on the same samples used to train it.

## 9. Interpretation

The results demonstrate that the public dataset contains microbiome-level information that can separate IBS and healthy-control samples under the tested modeling framework.

They do not establish:

- a clinical diagnostic test
- causal IBS-associated bacteria
- universal IBS biomarkers
- performance in an independent population

External validation would be required before making generalization or clinical claims.

## 10. Repository outputs

- `results/REPORT.md`
- result tables
- figures
- ML outputs
- QC outputs
- workflow documentation

Raw FASTQ and large intermediate QIIME 2 artifacts are not committed.

---

# Project 03 — Shotgun Metagenomics Taxonomic Profiling

## 1. Objective

Demonstrate shotgun metagenomic analysis of a real public human infant fecal WGS sample and compare two independent taxonomic classifiers.

The project emphasizes:

- WGS processing
- read QC
- taxonomic classification
- reference database management
- Kraken2
- Centrifuge
- independent classifier comparison
- reproducible compact outputs

## 2. Dataset

| Field | Value |
|---|---|
| BioProject | PRJNA273761 |
| Study | Metagenomes from human infant fecal samples with and without necrotizing enterocolitis |
| Run | SRR1779146 |
| BioSample | SAMN03295851 |
| Experiment | SRX858749 |
| Study accession | SRP052967 |
| Instrument | Illumina HiSeq 2000 |
| Strategy | WGS |
| Layout | Paired-end |
| Download size | ~1.5 GB |

The analysis intentionally uses one public run rather than pretending that a single sample represents the complete NEC cohort.

## 3. Workflow

```text
NCBI / ENA WGS
  ↓
Paired FASTQ
  ↓
FASTP
  ↓
Clean paired reads
  ├───────────────┐
  ↓               ↓
Kraken2         Centrifuge
  ↓               ↓
Taxonomic       Taxonomic
profile         profile
  └───────┬───────┘
          ↓
Classifier comparison
          ↓
Top taxa + QC + provenance
```

## 4. Read preprocessing

FASTP is used for:

- adapter detection
- quality processing
- generation of QC summaries

The same cleaned reads are passed to both classifiers so that classifier differences are not confounded by different input preprocessing.

## 5. Kraken2

The workflow uses a June 2026 Standard-8 Kraken2/Bracken database from the Langmead Lab AWS Open Data index infrastructure.

Database characteristics documented in the project:

- archive size: ~5.5 GB
- resulting database capped at 8 GB
- reference content includes bacterial, archaeal, viral, plasmid, human and UniVec Core sequences

The reduced database is a practical reproducibility trade-off and should not be treated as equivalent to every possible comprehensive reference database.

## 6. Centrifuge

Centrifuge uses the compressed bacteria + human + viral reference index hosted by the Langmead Lab AWS index infrastructure.

## 7. Verified results

Total fragments analyzed:

**7,954,717**

Kraken2:

- classified: 6,940,503
- unclassified: 1,014,214
- classified fraction: 87.25%
- unclassified fraction: 12.75%

Leading Kraken2 species:

**Enterobacter roggenkampii — 17.06% of total fragments**

Classifier comparison:

- top-10 species overlap: 7/10
- top-10 Jaccard similarity: 0.5385

## 8. Interpretation

The classifier comparison is methodological.

A species appearing in one classifier's output is not automatically biologically correct. Differences can arise from:

- reference databases
- taxonomy structure
- classification algorithms
- sequence ambiguity
- database completeness

## 9. Interpretation boundary

Because this is a single-run analysis, it cannot establish:

- NEC-associated taxa
- disease biomarkers
- prevalence
- cohort-level differences
- causality

A valid NEC comparison requires the full study cohort, consistent sample metadata, appropriate compositional/statistical methods and multiple-testing correction.

## 10. Reproducibility

The workflow:

1. Downloads the public FASTQ pair.
2. Runs FASTP.
3. Downloads the pinned Kraken2 database.
4. Runs Kraken2.
5. Removes the large Kraken2 database before obtaining the Centrifuge index.
6. Runs Centrifuge on the same cleaned reads.
7. Generates compact derived tables.
8. Keeps large raw/intermediate data outside Git.

---

# Project 04 — Nextflow / nf-core RNA-seq Workflow Engineering

## 1. Objective

Validate a production-style RNA-seq workflow using Nextflow and nf-core.

This project is about **workflow engineering**, not biological interpretation.

It demonstrates:

- Nextflow execution
- nf-core usage
- Docker reproducibility
- parameterization
- test-data validation
- structured outputs
- automated execution validation

## 2. Pipeline

**nf-core/rnaseq 3.27.0**

The project uses the maintained nf-core RNA-seq test profile.

## 3. Workflow

```text
nf-core/rnaseq test data
  ↓
Nextflow
  ↓
Docker containers
  ↓
Quality control
  ↓
Read processing
  ↓
Strandedness inference
  ↓
Alignment / quantification
  ↓
Expression outputs
  ↓
QC reports
```

## 4. Reproducibility configuration

| Component | Value |
|---|---|
| Pipeline | nf-core/rnaseq |
| Version | 3.27.0 |
| Workflow engine | Nextflow |
| CI execution version | 26.04.6 |
| Runtime | Docker |
| Test profile | test,docker |
| Output directory | results |

## 5. Core command

```bash
nextflow run nf-core/rnaseq \
  -r 3.27.0 \
  -profile test,docker \
  --outdir results
```

For repeated local execution:

```bash
nextflow run nf-core/rnaseq \
  -r 3.27.0 \
  -profile test,docker \
  --outdir results \
  -resume
```

## 6. Validation

The completed workflow validation produced:

- successful nf-core test execution
- structured `results/` output
- reproducible containerized execution

Verified artifact:

- Name: `project04-nfcore-results`
- Size: 50,007,842 bytes
- SHA-256: `343073a039e4408d5f710e30592294c1c6c30b9faa84881dfb0e94668da1855d`

The first test attempt failed because the pipeline required an explicit output directory. The command was corrected to include `--outdir results`, after which the full test succeeded.

## 7. Engineering lessons

This project demonstrates why workflow engineering requires explicit control of:

- pipeline versions
- parameters
- container environments
- output paths
- test data
- resource assumptions
- resumability

## 8. Scope boundary

The nf-core test dataset is not used to make biological claims.

The project demonstrates execution reliability and reproducibility. Project 06 is the separate biological RNA-seq differential-expression project.

---

# Project 05 — Bioinformatics + Machine Learning

## 1. Objective

Build a machine-learning workflow for distinguishing breast cancer tissue from normal breast tissue using public transcriptomic data.

The central technical goal is to demonstrate **leakage-aware model evaluation** rather than simply obtaining a high classification score.

## 2. Dataset

| Field | Value |
|---|---|
| GEO | GSE42568 |
| Title | Breast Cancer Gene Expression Analysis |
| Organism | Homo sapiens |
| Total samples | 121 |
| Breast cancer | 104 |
| Normal | 17 |
| Platform | GPL570 |
| Array | Affymetrix Human Genome U133 Plus 2.0 |
| Data type | Expression profiling by array |

The analysis uses the processed GEO series matrix rather than the large raw CEL archive.

## 3. Workflow

```text
GEO GSE42568
  ↓
Download processed series matrix
  ↓
Extract sample labels
  ↓
Expression matrix processing
  ↓
Zero-variance filtering
  ↓
Stratified cross-validation
  ↓
Feature selection inside training folds
  ↓
Standardization
  ↓
Logistic Regression
  ↓
Random Forest
  ↓
Out-of-fold predictions
  ↓
ROC-AUC / PR-AUC / accuracy metrics
  ↓
Exploratory feature ranking
```

## 4. Data processing

The workflow:

1. Downloads the public series matrix.
2. Parses the expression matrix.
3. Uses GEO sample metadata to assign class labels.
4. Removes zero-variance features.
5. Performs feature selection inside each training fold.
6. Standardizes selected features where required.
7. Fits the classifiers.
8. Produces out-of-fold predictions.

## 5. Leakage prevention

The feature-selection procedure is intentionally placed **inside cross-validation**.

For every training fold:

1. Identify non-constant features.
2. Calculate ANOVA F-scores using training data.
3. Select the top 100 features.
4. Standardize the selected features.
5. Fit the classifier.

The held-out fold is transformed using parameters learned from the training fold.

This prevents information from the test fold from influencing feature selection.

## 6. Models

### Logistic Regression

L2-regularized Logistic Regression.

### Random Forest

Random Forest with:

- 500 trees
- balanced class weighting

## 7. Evaluation

Metrics:

- ROC-AUC
- Average Precision / PR-AUC
- Accuracy
- Balanced Accuracy

Evaluation uses stratified 5-fold cross-validation.

## 8. Verified results

Dataset:

- 121 samples
- 104 breast cancer
- 17 normal
- 54,579 non-constant probes

### Logistic Regression

| Metric | Value |
|---|---:|
| ROC-AUC | 0.9802 |
| Average Precision | 0.9964 |
| Accuracy | 0.9752 |
| Balanced Accuracy | 0.9118 |

### Random Forest

| Metric | Value |
|---|---:|
| ROC-AUC | 0.9740 |
| Average Precision | 0.9953 |
| Accuracy | 0.9669 |
| Balanced Accuracy | 0.9070 |

## 9. Feature ranking

The final feature ranking is generated separately after cross-validation.

It is therefore an exploratory interpretation of the final fitted model and should not be treated as an unbiased estimate of predictive performance.

## 10. Interpretation

The high scores demonstrate strong separation between breast cancer and normal samples within this public dataset.

They do not establish:

- a clinical diagnostic test
- independently validated biomarkers
- causal genes
- generalization to other cohorts

Independent external validation would be required for those claims.

---

# Project 06 — RNA-seq Differential Expression

## 1. Objective

Analyze paired human CD4 T-cell bulk RNA-seq data from oral mucosa and blood while accounting for subject-level pairing.

The project demonstrates:

- public GEO count-matrix retrieval
- sample-subset definition
- metadata construction
- paired experimental design
- low-count filtering
- DESeq2 normalization
- Wald testing
- multiple-testing correction
- PCA
- differential-expression reporting

## 2. Dataset

| Field | Value |
|---|---|
| GEO | GSE116139 |
| Title | A human TH17 population with a tissue-resident signature in healthy and inflamed oral mucosal tissues [Bulk RNA-seq] |
| Organism | Homo sapiens |
| Platform | Illumina HiSeq 2500 |
| Full series | 28 samples |
| Project subset | matched CD69− samples |
| Analysis samples | 18 |
| Subjects | 9 |
| Comparison | oral mucosa vs blood |

The full GEO series contains additional sample types and experimental components. This project deliberately restricts the analysis to matched CD69− samples.

## 3. Sample design

The analysis contains nine subjects with matched mucosa and blood samples.

Subjects:

- 19
- 34
- 40
- 42
- 43
- 47
- 49
- 53
- 56

Total:

- 9 mucosa samples
- 9 blood samples
- 18 paired samples

## 4. Statistical design

The model is:

`~ subject + tissue`

The subject term accounts for inter-individual variation.

The tissue term tests the biological contrast:

**mucosa vs blood**

The contrast is explicitly:

`tissue = mucosa - blood`

## 5. Filtering

Low-count genes are filtered using:

`rowSums(counts >= 10) >= 9`

This retains genes with at least 10 counts in at least half of the 18 samples.

## 6. Differential-expression method

DESeq2 is used for:

- library-size normalization
- dispersion estimation
- model fitting
- Wald testing

Multiple testing is controlled using Benjamini–Hochberg adjusted p-values.

Significance threshold:

- adjusted p-value < 0.05
- absolute log2 fold change ≥ 1

## 7. Workflow

```text
GEO processed count matrix
  ↓
Resolve sample/library identifiers
  ↓
Select matched CD69− samples
  ↓
Build subject + tissue metadata
  ↓
Low-count filtering
  ↓
DESeq2 dataset
  ↓
Normalization
  ↓
Wald test
  ↓
BH multiple-testing correction
  ↓
PCA
  ↓
Differential-expression table
  ↓
Volcano plot
  ↓
Summary report
```

## 8. Documented results

The project documentation records:

- 18 samples
- 9 subjects
- 11,696 genes after low-count filtering
- 519 significant genes
- 294 significantly upregulated genes
- 225 significantly downregulated genes

| Result | Value |
|---|---:|
| Samples | 18 |
| Subjects | 9 |
| Genes after filtering | 11,696 |
| Significant genes | 519 |
| Upregulated | 294 |
| Downregulated | 225 |

The detailed result files are intended to include:

- differential-expression table
- normalized counts
- PCA
- volcano plot
- sample/library mapping
- summary report

## 9. Biological interpretation boundary

The analysis identifies expression differences associated with tissue in this specific public research dataset.

It does not establish:

- clinical biomarkers
- diagnostic utility
- causal mechanisms
- universal tissue-specific markers
- generalization to unrelated cohorts

Independent datasets and biological validation are required for stronger claims.

## 10. Reproducibility

The project records:

- GEO accession
- sample subset
- subject identifiers
- tissue labels
- statistical design
- filtering threshold
- DESeq2 analysis
- output structure

Large generated matrices and raw sequencing files should remain outside the repository when they are too large for practical GitHub storage.

---

# Cross-Project Technical Summary

## Data types covered

| Project | Data type | Main analysis |
|---|---|---|
| 01 | 16S amplicon | Microbiome profiling |
| 02 | 16S amplicon | IBS classification |
| 03 | Shotgun WGS | Taxonomic profiling |
| 04 | RNA-seq test data | Workflow engineering |
| 05 | Microarray transcriptomics | Machine learning |
| 06 | Bulk RNA-seq | Differential expression |

## Main tools demonstrated

### Sequencing / bioinformatics

- SRA Toolkit
- FastQC
- MultiQC
- FASTP
- QIIME 2
- SILVA
- nf-core/ampliseq
- nf-core/rnaseq
- Nextflow
- Docker
- Kraken2
- Centrifuge
- DESeq2

### Programming

- Python
- R
- Bash
- Linux shell

### Data science

- Pandas
- NumPy
- scikit-learn
- Logistic Regression
- Random Forest
- cross-validation
- feature selection
- ROC-AUC
- Average Precision
- statistical testing
- multiple-testing correction

## Reproducibility principles

Across the portfolio:

1. Public accessions are recorded.
2. Raw sequencing data are not unnecessarily committed to Git.
3. Software versions are documented where important.
4. Parameters are recorded.
5. QC is performed before interpretation.
6. Cross-validation is used for supervised learning.
7. Feature selection is performed without test-fold leakage.
8. Paired experimental designs are modeled explicitly.
9. Single-sample results are not presented as cohort-level findings.
10. Biological interpretation is separated from computational observations.
11. Results are reported only when supported by an executed analysis.
12. Large intermediate files are kept outside the repository.

## Portfolio progression

The six projects intentionally increase in analytical complexity:

```text
Project 01
16S workflow fundamentals
        ↓
Project 02
Microbiome statistics + machine learning
        ↓
Project 03
Shotgun metagenomics + classifier comparison
        ↓
Project 04
Production workflow engineering
        ↓
Project 05
Transcriptomics + leakage-safe machine learning
        ↓
Project 06
Paired bulk RNA-seq + differential expression
```

This progression demonstrates practical capability across sequencing technologies, computational workflows, statistical analysis, machine learning and reproducible bioinformatics.
