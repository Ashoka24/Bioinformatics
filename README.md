# Bioinformatics Projects

I work across microbiome analysis, sequencing workflows, transcriptomics and machine learning. This repository brings together projects built around public biological datasets, with an emphasis on clear methods, reproducible analysis and careful interpretation of results.

## Projects

| Project | Focus | Tools |
|---|---|---|
| [16S rRNA Gut Microbiome Profiling](16s-gut-microbiome/) | Processing public amplicon data, read quality checks, taxonomy and microbial community profiling | FastQC, MultiQC, nf-core/ampliseq, QIIME 2, SILVA |
| [IBS Microbiome Analysis and Machine Learning](ibs-microbiome-ml/) | Microbiome features, diversity analysis and exploratory model evaluation for IBS-related data | QIIME 2, Deblur, Python, scikit-learn |
| [Shotgun Metagenomic Profiling](shotgun-metagenomics/) | Taxonomic classification of public sequencing reads and comparison of classifiers | fastp, Kraken 2, Centrifuge |
| [Reproducible RNA-seq Pipeline](nfcore-rnaseq-pipeline/) | Running a containerized bulk RNA-seq workflow | Nextflow, nf-core/rnaseq, Docker |
| [Transcriptomics Classification with Machine Learning](transcriptomics-machine-learning/) | Gene-expression data preparation, feature selection and classification evaluation | Python, Pandas, scikit-learn |
| [Paired RNA-seq Differential Expression](rnaseq-differential-expression/) | Matched-tissue differential expression and multiple-testing correction | R, DESeq2 |
| [Whole-Exome Sequencing Variant Analysis](wes-variant-analysis/) | Tumor/normal variant analysis and annotation | nf-core/sarek, Mutect2, VEP, Nextflow |
| [Single-Cell RNA-seq Analysis of PBMCs](single-cell-rnaseq-pbmcs/) | Cell quality control, normalization, dimensionality reduction, clustering and marker analysis | Python, Scanpy, AnnData |

## How the projects are documented

Each project describes its data source, main analysis steps, software and parameters, and the results available for review. Where a project uses a small public dataset to demonstrate a workflow, the conclusions are kept within what that dataset can support.

- [Technical project documentation](docs/PROJECT_DOCUMENTATION.md)
- [AWS omics architecture](docs/AWS_OMICS_ARCHITECTURE.md)
- [Cloud and AWS resources](cloud/aws/)

## Skills

**Bioinformatics:** 16S rRNA analysis, microbiome profiling, shotgun metagenomics, bulk RNA-seq, single-cell RNA-seq and variant analysis.

**Programming and analysis:** Python, R, SQL, Bash, statistical testing, data processing, feature engineering, machine learning and visualization.

**Workflow tools:** Linux, Nextflow, nf-core, Docker, Git and reproducible pipeline development.

## License

Code and documentation in this repository are released under the [MIT License](LICENSE), unless a project file states otherwise. Third-party datasets, reference databases, software and other external materials remain subject to their own licences and terms.

## Notes

- Data accessions, software versions and important parameters are documented with the relevant project.
- Large raw datasets and intermediate files are kept out of Git where appropriate.
- Single-sample demonstrations are described as workflow examples, not as cohort-level biological findings.
