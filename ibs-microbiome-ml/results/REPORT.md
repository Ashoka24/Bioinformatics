# Actual outcome — IBS microbiome cohort

> **Result status:** The metrics below are from the earlier analysis and are retained as a historical snapshot. The pipeline has since been corrected so feature filtering and transformations are fitted inside each training fold. Do not present the AUC, accuracy, or diversity values below as the verified output of the corrected pipeline. The updated run is publishing its outputs as a GitHub Actions artifact.

Public-data-only re-analysis of PRJNA637763.

## Cohort
- Samples analyzed: 111
- IBS: 85
- Healthy controls: 26
- Genus features after prevalence filtering: 131

## Alpha diversity
- Mean observed features, IBS: 275.38
- Mean observed features, HC: 301.96
- Mean Shannon, IBS: 3.9586
- Mean Shannon, HC: 4.2491

## Classification
Five-fold stratified cross-validation.
- l1_logistic: ROC-AUC=0.9181; accuracy=0.8288; precision=0.9342; sensitivity=0.8353
- random_forest: ROC-AUC=0.8604; accuracy=0.7748; precision=0.7830; sensitivity=0.9765

These are independent re-analysis metrics, not clinical diagnostic validation.