# Project 06 — RNA-seq Differential Expression

Bulk RNA-seq analysis of paired human CD4 T-cell samples from oral mucosa and blood.

## Dataset

**NCBI GEO:** GSE116139  
**Organism:** Homo sapiens  
**Platform:** Illumina HiSeq 2500  
**Study:** A human TH17 population with a tissue-resident signature in healthy and inflamed oral mucosal tissues

The GEO study contains paired oral mucosa and blood CD4 T-cell RNA-seq samples from multiple subjects. This project uses the matched CD69− samples only and compares mucosa against blood within subject.

## Analysis

- Public processed gene-count matrix from GEO
- Matched CD69− samples
- Paired differential-expression design: subject + tissue
- Low-count filtering
- DESeq2 normalization and Wald testing
- Benjamini–Hochberg multiple-testing correction
- PCA for sample-level structure
- Differential-expression table and plots

## Workflow

GEO count matrix → sample selection → count filtering → DESeq2 → PCA / differential expression → interpretation

## Results

Results will be added only after the analysis has been executed and verified.

- Samples: 18 matched CD69− samples from 9 subjects
- Comparison: oral mucosa vs blood
- Statistical model: subject + tissue
- Significance threshold: adjusted p-value < 0.05 and |log2FC| ≥ 1

## Repository structure

06_rnaseq_differential_expression/
├── README.md
├── metadata/
│   └── DATASET.md
├── scripts/
│   └── run_deseq2.R
├── figures/
│   ├── 01_workflow.svg
│   └── 02_output_file_map.svg
└── results/
    ├── REPORT.md
    ├── differential_expression.tsv
    ├── normalized_counts.tsv
    └── figures/

## Notes

This is a transcriptomic differential-expression analysis of a public research dataset. The findings are not presented as clinical biomarkers or diagnostic evidence.

[Back to portfolio](../../)
