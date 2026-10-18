#!/usr/bin/env python3
"""Build descriptive IBS microbiome results and leakage-aware CV metrics."""
from collections import defaultdict
from pathlib import Path
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path("results_actual")
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
ML = ROOT / "ml"
FIGURES.mkdir(parents=True, exist_ok=True)
ML.mkdir(parents=True, exist_ok=True)

# Keep the feature-table header and every feature row. BIOM export includes
# comment lines before the "#OTU ID" header.
raw_lines = (TABLES / "feature-table.tsv").read_text(encoding="utf-8").splitlines()
header = next((line for line in raw_lines if line.startswith("#OTU ID")), None)
if header is None:
    raise SystemExit("Could not find the '#OTU ID' header in the exported feature table.")
samples = header.split("\t")[1:]
samples = [sample for sample in samples if sample]
data_lines = [line for line in raw_lines if line and not line.startswith("#")]

feature_rows = []
for line in data_lines:
    fields = line.split("\t")
    if len(fields) < len(samples) + 1:
        continue
    feature_rows.append([fields[0]] + [float(value or 0) for value in fields[1:len(samples) + 1]])

if not feature_rows or not samples:
    raise SystemExit("The feature table has no usable samples or feature rows.")

counts = pd.DataFrame(feature_rows, columns=["feature"] + samples).set_index("feature")
metadata = pd.read_csv("metadata/sample-metadata.tsv", sep="\t").set_index("sample-id")
missing = [sample for sample in samples if sample not in metadata.index]
if missing:
    raise SystemExit(f"Feature-table samples missing from metadata: {missing[:5]}")
metadata = metadata.loc[samples]
labels = metadata["group"].map({"HC": 0, "IBS": 1}).to_numpy()
if pd.isna(labels).any() or len(np.unique(labels)) != 2:
    raise SystemExit("Expected both IBS and HC labels for every feature-table sample.")

taxonomy = pd.read_csv(TABLES / "taxonomy.tsv", sep="\t").fillna("")
taxonomy_map = dict(zip(taxonomy["Feature ID"], taxonomy["Taxon"]))


def genus_name(lineage):
    parts = [part.strip() for part in lineage.split(";")]
    if len(parts) < 6 or not parts[5]:
        return "Unassigned"
    value = parts[5]
    return value.split("__", 1)[-1] if "__" in value else value


# Relative abundance is calculated per sample before the model pipeline.
# Prevalence filtering and log-ratio transformation are fitted/applied inside
# each cross-validation fold, so held-out samples do not choose model features.
relative = counts.div(counts.sum(axis=0).replace(0, np.nan), axis=1).fillna(0)
genus_values = defaultdict(lambda: np.zeros(len(samples), dtype=float))
for feature_id in relative.index:
    genus_values[genus_name(taxonomy_map.get(feature_id, ""))] += relative.loc[feature_id].to_numpy()

genus_relative = pd.DataFrame(genus_values, index=samples).T.T
if genus_relative.empty:
    raise SystemExit("No genus-level features could be built from the taxonomy table.")


class PrevalenceFilter(BaseEstimator, TransformerMixin):
    """Select genera present in more than the configured fraction of training samples."""

    def __init__(self, threshold=0.10):
        self.threshold = threshold

    def fit(self, X, y=None):
        matrix = np.asarray(X, dtype=float)
        prevalence = (matrix > 0).mean(axis=0)
        self.support_ = prevalence > self.threshold
        if not self.support_.any():
            self.support_[int(np.argmax(prevalence))] = True
        return self

    def transform(self, X):
        return np.asarray(X, dtype=float)[:, self.support_]


class CenteredLogRatio(BaseEstimator, TransformerMixin):
    """Apply a pseudocount log-ratio transform separately to each sample."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        logged = np.log(np.asarray(X, dtype=float) + 1e-6)
        return logged - logged.mean(axis=1, keepdims=True)


def make_pipeline(estimator):
    return Pipeline([
        ("prevalence", PrevalenceFilter(threshold=0.10)),
        ("clr", CenteredLogRatio()),
        ("scale", StandardScaler()),
        ("model", estimator),
    ])


cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
models = {
    "l1_logistic": make_pipeline(
        LogisticRegression(
            penalty="l1",
            solver="liblinear",
            max_iter=3000,
            class_weight="balanced",
        )
    ),
    "random_forest": make_pipeline(
        RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
            max_features="sqrt",
        )
    ),
}

results = []
for name, model in models.items():
    probabilities = cross_val_predict(
        model, genus_relative.to_numpy(), labels, cv=cv, method="predict_proba"
    )[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    results.append([
        name,
        roc_auc_score(labels, probabilities),
        accuracy_score(labels, predictions),
        precision_score(labels, predictions, zero_division=0),
        recall_score(labels, predictions, zero_division=0),
    ])

pd.DataFrame(
    results,
    columns=["model", "roc_auc", "accuracy", "precision", "sensitivity"],
).to_csv(ML / "cross_validation_metrics.tsv", sep="\t", index=False)

# Fit on the full cohort only for an exploratory feature-ranking table.
final_logistic = models["l1_logistic"].fit(genus_relative.to_numpy(), labels)
selected_mask = final_logistic.named_steps["prevalence"].support_
selected_genera = genus_relative.columns[selected_mask]
coefficients = final_logistic.named_steps["model"].coef_[0]
pd.DataFrame({
    "genus": selected_genera,
    "coefficient": coefficients,
    "abs_coefficient": np.abs(coefficients),
}).query("abs_coefficient > 0").sort_values(
    "abs_coefficient", ascending=False
).to_csv(ML / "l1_selected_genera.tsv", sep="\t", index=False)

# Diversity metrics are calculated from the full feature table, independently
# of the classification feature filter.
alpha_rows = []
for sample in samples:
    values = counts[sample].to_numpy()
    values = values[values > 0]
    proportions = values / values.sum()
    alpha_rows.append([
        sample,
        metadata.loc[sample, "group"],
        int((counts[sample] > 0).sum()),
        -sum(value * math.log(value) for value in proportions),
        1 - sum(value * value for value in proportions),
    ])
alpha = pd.DataFrame(
    alpha_rows,
    columns=["sample", "group", "observed_features", "shannon", "simpson"],
)
alpha.to_csv(TABLES / "alpha_diversity.tsv", sep="\t", index=False)

top_genera = genus_relative.mean(axis=0).sort_values(ascending=False).head(15).index
genus_relative.loc[:, top_genera].plot(
    kind="bar", stacked=True, figsize=(12, 6), width=0.9
)
plt.ylabel("Relative abundance")
plt.title("Most abundant genera across analyzed samples")
plt.tight_layout()
plt.savefig(FIGURES / "genus_relative_abundance.png", dpi=180)
plt.close()

full_prevalence_count = int(((genus_relative > 0).mean(axis=0) > 0.10).sum())
report = [
    "# Actual outcome — IBS microbiome cohort",
    "",
    "Public-data-only re-analysis of PRJNA637763.",
    "",
    "## Cohort",
    f"- Samples analyzed: {len(samples)}",
    f"- IBS: {int((labels == 1).sum())}",
    f"- Healthy controls: {int((labels == 0).sum())}",
    f"- Genera present in more than 10% of the full cohort: {full_prevalence_count}",
    "",
    "## Alpha diversity",
    f"- Mean observed features, IBS: {alpha.loc[alpha.group == 'IBS', 'observed_features'].mean():.2f}",
    f"- Mean observed features, HC: {alpha.loc[alpha.group == 'HC', 'observed_features'].mean():.2f}",
    f"- Mean Shannon, IBS: {alpha.loc[alpha.group == 'IBS', 'shannon'].mean():.4f}",
    f"- Mean Shannon, HC: {alpha.loc[alpha.group == 'HC', 'shannon'].mean():.4f}",
    "",
    "## Classification",
    "Metrics use five-fold stratified cross-validation. The prevalence filter, log-ratio transform, and standardization are fitted within each training fold.",
]
for row in results:
    report.append(
        f"- {row[0]}: ROC-AUC={row[1]:.4f}; accuracy={row[2]:.4f}; "
        f"precision={row[3]:.4f}; sensitivity={row[4]:.4f}"
    )
report.extend([
    "",
    "The genus coefficients in l1_selected_genera.tsv come from a separate model fitted to the full cohort and are exploratory, not an unbiased performance estimate.",
    "This is a public-data re-analysis, not clinical diagnostic validation. Results depend on the study metadata, preprocessing choices, and the selected cohort.",
])
(ROOT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
print("\n".join(report))
