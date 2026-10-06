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

## Project 04 — Production-style Nextflow / nf-core

Project 04 moves from individual analysis scripts to **workflow engineering**. It validates nf-core/rnaseq 3.27.0 using the public nf-core test profile, Docker containers and GitHub Actions CI.

The project is **completed**: GitHub Actions run #2 succeeded and the generated CI artifact was verified.

See the [Project 04 documentation](projects/04_nfcore_pipeline/).

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
