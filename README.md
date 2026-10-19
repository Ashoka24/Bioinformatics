# Bioinformatics Portfolio

Bioinformatics and computational biology projects covering microbiome profiling, metagenomics, transcriptomics, machine learning, and variant analysis. Each project includes its own workflow, documented methods, results, and supporting evidence.

## Workflow status

[![Project 01 — 16S](https://github.com/Ashoka24/Bioinformatics/actions/workflows/16s-actual-outcome.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/16s-actual-outcome.yml) [![Project 02 — IBS](https://github.com/Ashoka24/Bioinformatics/actions/workflows/02-ibs-microbiome.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/02-ibs-microbiome.yml) [![Project 03 — Shotgun](https://github.com/Ashoka24/Bioinformatics/actions/workflows/03-shotgun-metagenomics.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/03-shotgun-metagenomics.yml) [![Project 04 — nf-core RNA-seq](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project04_nfcore.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project04_nfcore.yml)

[![Project 05 — ML](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project05_ml.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project05_ml.yml) [![Project 06 — RNA-seq](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project06_rnaseq.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project06_rnaseq.yml) [![Project 07 — WES](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project07_wes.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project07_wes.yml) [![Project 08 — scRNA-seq](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project-08-scrnaseq.yml/badge.svg)](https://github.com/Ashoka24/Bioinformatics/actions/workflows/project-08-scrnaseq.yml)

## Featured analysis projects

| Project | What it covers | Main tools |
|---|---|---|
| [16S rRNA Gut Microbiome Profiling](16s-gut-microbiome/) | Public SRA data, read QC, amplicon processing, taxonomy and microbiome profiling | FastQC, MultiQC, nf-core/ampliseq, QIIME 2, SILVA |
| [IBS Microbiome Analysis and Machine Learning](ibs-microbiome-ml/) | IBS and healthy-control cohort, genus-level features, diversity and model evaluation | QIIME 2, Deblur, Python, scikit-learn |
| [Shotgun Metagenomic Profiling](shotgun-metagenomics/) | Public WGS read classification and comparison of taxonomic classifiers | fastp, Kraken2, Centrifuge |
| [Reproducible RNA-seq Pipeline](nfcore-rnaseq-pipeline/) | Containerized workflow execution and CI validation | Nextflow, nf-core/rnaseq, Docker, GitHub Actions |
| [Transcriptomics Classification with Machine Learning](transcriptomics-machine-learning/) | Breast cancer expression dataset, leakage-aware feature selection and classification evaluation | Python, Pandas, scikit-learn |
| [Paired RNA-seq Differential Expression](rnaseq-differential-expression/) | Matched tissue analysis, DESeq2 and multiple-testing correction | R, DESeq2 |
| [Whole-Exome Sequencing Variant Analysis](wes-variant-analysis/) | Matched tumor/normal variant-calling workflow and annotation | nf-core/sarek, Mutect2, VEP, Nextflow |
| [Single-Cell RNA-seq Analysis of PBMCs](single-cell-rnaseq-pbmcs/) | Cell QC, filtering, normalization, PCA, UMAP, clustering and marker ranking | Python, Scanpy, AnnData |

## Evidence and reproducibility

Project READMEs include the relevant workflow, data source, analysis steps, and available result summaries or QC evidence. Figures labelled as summaries are generated from recorded analysis outputs; they are not presented as original FastQC/MultiQC screenshots.

- [Technical project documentation](docs/PROJECT_DOCUMENTATION.md)
- [AWS omics architecture](docs/AWS_OMICS_ARCHITECTURE.md)
- [Cloud and AWS resources](cloud/aws/)

## Skills demonstrated

**Bioinformatics:** 16S rRNA analysis, microbiome profiling, shotgun metagenomics, bulk RNA-seq, single-cell RNA-seq, WES variant analysis.

**Programming and statistics:** Python, R, SQL, Bash, data processing, statistical testing, feature engineering, machine learning, data visualization.

**Workflow engineering:** Linux, Nextflow, nf-core, Docker, Git/GitHub, GitHub Actions, reproducible pipelines and QC reporting.

## License

The code and accompanying documentation in this repository are released under the [MIT License](LICENSE), unless a project file states otherwise. Third-party datasets, reference databases, software, and externally sourced materials remain subject to their own licences and terms; please check the relevant source before reuse.

## Notes

- Dataset accessions, software versions, and key parameters are documented in the individual project folders.
- Large raw datasets and intermediate files are kept out of Git when appropriate.
- Results are reported within the limits of the underlying dataset; single-sample analyses are not presented as cohort-level conclusions.

