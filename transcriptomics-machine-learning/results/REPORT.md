# Transcriptomics Classification Results

## Dataset

- GEO accession: GSE42568
- Samples: 121
- Normal: 17
- Breast cancer: 104
- Non-constant probes in the full matrix: 54579
- Cross-validation: stratified 5-fold, shuffle=True, random_state=42
- Variance filtering and top-100 ANOVA F-score selection are fitted within each training fold

## Cross-validated performance

| Model | ROC-AUC | Average Precision | Accuracy | Balanced Accuracy |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.9802 | 0.9964 | 0.9752 | 0.9118 |
| Random Forest | 0.9740 | 0.9953 | 0.9669 | 0.9070 |

## Interpretation

The reported metrics are out-of-fold predictions and therefore are not based on predictions from models trained on the corresponding test folds.

The feature ranking is exploratory because the final ranking models are fit on all samples after cross-validation. It should not be interpreted as an independently validated biomarker list.

The task is tissue-class classification within GSE42568. It is not a clinical diagnostic validation study.
