# IBS Microbiome Analysis and Machine Learning

## Analysis evidence

The committed figure and `results/` files are a historical snapshot. Their previously reported model metrics are not the verified output of the corrected pipeline. The latest successful GitHub Actions run re-executed the analysis and uploaded the fresh output as the `project02-ibs-results` artifact. Read-processing statistics in the committed snapshot are available in `results/qc/deblur-stats/stats.csv`.

![IBS cohort analysis evidence](results/figures/03_read_processing_evidence.svg)

## Overview figure

![IBS microbiome classification results overview](figures/03_overview.svg)
Public-data-only cohort analysis using PRJNA637763, a human gut 16S rRNA dataset containing 85 IBS samples and 26 healthy controls. The study used V1–V2 amplicon sequencing on Illumina MiSeq and was explicitly designed for microbiome-based IBS prediction.

## Workflow figure

![IBS microbiome workflow](figures/01_workflow.svg)

![Output file map](figures/02_output_file_map.svg)

## Objectives
1. Build a 16S feature table from public SRA/ENA reads.
2. Summarize alpha diversity and taxonomic composition.
3. Compare IBS and healthy-control samples descriptively.
4. Evaluate genus-level classifiers with stratified cross-validation.
5. Record the model metrics and ranked genera.

## Analysis
- Public source: NCBI BioProject PRJNA637763
- Study: Usefulness of Machine Learning-Based Gut Microbiome Analysis for Identifying Patients with Irritable Bowels Syndrome
- Samples: 85 IBS + 26 healthy controls
- Region: V1–V2
- Platform: Illumina MiSeq, paired-end
- Denoising: QIIME 2 Deblur on forward reads
- Taxonomy: SILVA 138 99% classifier
- ML: scikit-learn logistic regression and random forest with stratified cross-validation

This is an independent re-analysis of public data, not a reproduction of the original paper's exact preprocessing or model. The genus-prevalence filter, log-ratio transform and standardization are fitted within each training fold. The separately reported L1 genus ranking is fitted on the full cohort and is exploratory; it is not used to estimate cross-validation performance.

## Outputs
- results/REPORT.md
- results/tables/
- results/figures/
- results/ml/
- results/qc/

Raw FASTQ and intermediate QIIME artifacts are intentionally not committed.

## Run the analysis

From the repository root, run:

```bash
bash ibs-microbiome-ml/scripts/02_run_ibs_analysis.sh
```

The script downloads public reads and runs the QIIME 2 steps in Docker. Temporary files and fresh results are written under `work/`, `metadata/` and `results_actual/` at the repository root. GitHub Actions uploads `results_actual/` as the `project02-ibs-results` artifact; it does not copy those fresh outputs into the committed `results/` directory. Use the artifact from the latest successful run for current metrics.
