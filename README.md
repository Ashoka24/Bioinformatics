# Bioinformatics Portfolio

This repository contains reproducible bioinformatics projects covering NGS, metagenomics, microbiome analysis, Python/R, Linux, Nextflow, Docker and biological data interpretation.

## Projects

### 1. NCBI Human Gut 16S — End-to-End Pipeline

A human-stool 16S rRNA experiment using an openly available NCBI SRA run, built to mirror the operational IOM workflow and extend it through reproducible public-data retrieval, QC, nf-core/ampliseq, QIIME 2 downstream analysis and biological interpretation.

- NCBI SRA run: SRR26534086
- BioSample: SAMN37943185
- BioProject: PRJNA1031545
- Illumina MiSeq paired-end V3–V4 16S
- FastQC + MultiQC
- SRA Toolkit
- nf-core/ampliseq 2.11.0
- Docker
- DADA2
- SILVA taxonomy
- QIIME 2
- Shannon / observed ASVs
- Bray–Curtis / PCoA for multi-sample expansion
- reproducible VM/storage paths
- checksums and execution logs

See: `projects/ncbi_gut_16s/`

### 2. 16S Microbiome Analysis — Moving Pictures

A smaller inspectable public-data example demonstrating downstream microbiome calculations, diversity and ordination.

## Working principle

```text
Biological question
      ↓
Public/traceable data
      ↓
Raw-data provenance
      ↓
QC
      ↓
Reproducible pipeline
      ↓
Post-QC
      ↓
Statistics
      ↓
Visualization
      ↓
Biological interpretation
      ↓
Limitations
```

The objective is to show not only which tools were used, but why each step was performed and what was learned from the data.
