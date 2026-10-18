#!/usr/bin/env python3
"""Build descriptive IBS microbiome results and leakage-aware CV metrics."""
from collections import defaultdict
from pathlib import Path
import html
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

genus_relative = pd.DataFrame(genus_values, index=samples)
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

# Regenerate the evidence graphic from this run so it cannot silently display
# metrics from an older model implementation.
metric_values = {row[0]: row[1] for row in results}
cards = [
    ("Samples", str(len(samples))),
    ("IBS", str(int((labels == 1).sum()))),
    ("Healthy controls", str(int((labels == 0).sum()))),
    ("Genera present in >10% of samples", str(full_prevalence_count)),
    ("L1 logistic ROC-AUC", f"{metric_values['l1_logistic']:.4f}"),
    ("Random forest ROC-AUC", f"{metric_values['random_forest']:.4f}"),
]
svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="390" viewBox="0 0 1100 390" role="img">',
    '<rect width="1100" height="390" rx="18" fill="#ffffff" stroke="#d7e0e8"/>',
    '<rect width="1100" height="88" rx="18" fill="#17324d"/>',
    '<rect y="68" width="1100" height="20" fill="#17324d"/>',
    '<text x="30" y="38" font-family="Arial,Helvetica,sans-serif" font-size="25" font-weight="700" fill="#ffffff">IBS cohort analysis evidence</text>',
    '<text x="30" y="65" font-family="Arial,Helvetica,sans-serif" font-size="15" fill="#d8e5ef">Public 16S re-analysis · five-fold stratified cross-validation</text>',
]
for index, (label, value) in enumerate(cards):
    column = index % 3
    row = index // 3
    x = 28 + column * 354
    y = 112 + row * 126
    svg.extend([
        f'<rect x="{x}" y="{y}" width="330" height="104" rx="12" fill="#f4f7fb" stroke="#d8e0ea"/>',
        f'<text x="{x + 18}" y="{y + 42}" font-family="Arial,Helvetica,sans-serif" font-size="27" font-weight="700" fill="#17324d">{html.escape(value)}</text>',
        f'<text x="{x + 18}" y="{y + 73}" font-family="Arial,Helvetica,sans-serif" font-size="14" fill="#526477">{html.escape(label)}</text>',
    ])
svg.extend([
    '<text x="1070" y="375" text-anchor="end" font-family="Arial,Helvetica,sans-serif" font-size="11" fill="#718096">Generated from this run’s outputs · not a FastQC screenshot</text>',
    '</svg>',
])
(FIGURES / "03_read_processing_evidence.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")

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
