# Verified Run

- Dataset: NCBI GEO GSE116139
- Input: 18 matched CD69− bulk RNA-seq samples
- Subjects: 9
- Comparison: oral mucosa vs blood
- Design: `~ subject + tissue`
- Genes after low-count filtering: 11,696
- Significant genes: 519
- Threshold: adjusted p-value < 0.05 and |log2FC| >= 1
- Significant upregulated genes: 294
- Significant downregulated genes: 225

## Top ranked genes

| Gene | log2FC | p-value | adjusted p-value |
|---|---:|---:|---:|
| ENSG00000067082 | 1.3532 | 2.3365e-49 | 2.7328e-45 |
| ENSG00000163599 | 1.7167 | 5.8727e-31 | 3.4343e-27 |
| ENSG00000125740 | 3.8223 | 2.2593e-30 | 8.8083e-27 |
| ENSG00000120738 | 4.7488 | 1.0451e-25 | 3.0560e-22 |
| ENSG00000143384 | 1.3106 | 1.5140e-25 | 3.5415e-22 |
| ENSG00000120129 | 1.7307 | 7.1655e-24 | 1.3968e-20 |
| ENSG00000026508 | 0.9124 | 1.8433e-22 | 3.0799e-19 |
| ENSG00000232810 | 1.7167 | 2.1137e-22 | 3.0903e-19 |
| ENSG00000135046 | 0.8217 | 7.5667e-22 | 9.8333e-19 |
| ENSG00000163660 | 0.7698 | 1.3643e-21 | 1.596e-18 |
| ENSG00000026025 | 1.1085 | 2.7852e-21 | 2.9614e-18 |
| ENSG00000087074 | 1.6205 | 7.3357e-21 | 7.1499e-18 |
| ENSG00000136527 | 0.5613 | 3.4394e-19 | 3.0944e-16 |
| ENSG00000164442 | 1.6358 | 8.0985e-19 | 6.7657e-16 |
| ENSG00000057657 | 1.5007 | 1.12996e-18 | 8.8107e-16 |

The complete differential-expression table, normalized counts, PCA, volcano plot, and library mapping were generated and verified in the successful Project 06 workflow artifact.