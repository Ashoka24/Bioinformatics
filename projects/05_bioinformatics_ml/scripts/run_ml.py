#!/usr/bin/env python3
import gzip
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"

MATRIX = DATA / "GSE42568_series_matrix.txt.gz"
RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)


def parse_sample_titles(path):
    titles = None
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("!Sample_title"):
                fields = line.rstrip("\n").split("\t")
                titles = [x.strip().strip('"') for x in fields[1:]]
                break
    if titles is None:
        raise RuntimeError("Could not find !Sample_title in GEO matrix")
    return titles


def load_expression(path, sample_titles):
    header = None
    rows = []
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.startswith("!series_matrix_table_begin"):
                header = [x.strip().strip('"') for x in next(handle).rstrip("\n").split("\t")]
                break
        if header is None:
            raise RuntimeError("Could not find series matrix table")

        expected = ["ID_REF"] + sample_titles
        if len(header) != len(expected):
            raise RuntimeError(
                f"Header/sample mismatch: {len(header)} columns vs {len(expected)} expected"
            )

        for line in handle:
            if line.startswith("!series_matrix_table_end"):
                break
            parts = line.rstrip("\n").split("\t")
            if len(parts) != len(header):
                continue
            rows.append(parts)

    df = pd.DataFrame(rows, columns=header)
    df["ID_REF"] = df["ID_REF"].astype(str)
    for col in header[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(axis=0, how="any")
    df = df.drop_duplicates(subset="ID_REF").set_index("ID_REF")
    return df


def make_labels(titles):
    labels = []
    for title in titles:
        low = title.lower()
        if "normal breast" in low:
            labels.append(0)
        elif "breast cancer" in low:
            labels.append(1)
        else:
            raise RuntimeError(f"Unexpected sample title: {title}")
    return np.asarray(labels, dtype=int)


def evaluate(name, estimator, X, y, cv):
    pred = cross_val_predict(estimator, X, y, cv=cv, method="predict")
    prob = cross_val_predict(estimator, X, y, cv=cv, method="predict_proba")[:, 1]
    return {
        "model": name,
        "roc_auc": roc_auc_score(y, prob),
        "average_precision": average_precision_score(y, prob),
        "accuracy": accuracy_score(y, pred),
        "balanced_accuracy": balanced_accuracy_score(y, pred),
        "predictions": pred,
        "probabilities": prob,
    }


def main():
    if not MATRIX.exists():
        raise FileNotFoundError(MATRIX)

    titles = parse_sample_titles(MATRIX)
    expression = load_expression(MATRIX, titles)

    if expression.shape[1] != len(titles):
        raise RuntimeError("Expression matrix sample count does not match metadata")

    y = make_labels(titles)
    X = expression.T

    # Remove features that are constant across all samples.
    nonzero_var = X.var(axis=0) > 0
    X = X.loc[:, nonzero_var]

    k = min(100, X.shape[1])
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    models = {
        "Logistic Regression": Pipeline(
            [
                ("select", SelectKBest(score_func=f_classif, k=k)),
                ("scale", StandardScaler()),
                ("model", LogisticRegression(max_iter=5000, random_state=42)),
            ]
        ),
        "Random Forest": Pipeline(
            [
                ("select", SelectKBest(score_func=f_classif, k=k)),
                ("model", RandomForestClassifier(
                    n_estimators=500,
                    random_state=42,
                    class_weight="balanced",
                    n_jobs=-1,
                )),
            ]
        ),
    }

    evaluations = {}
    metric_rows = []
    for name, model in models.items():
        result = evaluate(name, model, X, y, cv)
        evaluations[name] = result
        metric_rows.append(
            {
                "model": name,
                "roc_auc": result["roc_auc"],
                "average_precision": result["average_precision"],
                "accuracy": result["accuracy"],
                "balanced_accuracy": result["balanced_accuracy"],
            }
        )

    metrics = pd.DataFrame(metric_rows)
    metrics.to_csv(RESULTS / "metrics.tsv", sep="\t", index=False)

    # Fit the models once on all samples only for exploratory feature ranking.
    feature_rows = []
    for name, model in models.items():
        model.fit(X, y)
        selected = model.named_steps["select"]
        mask = selected.get_support()
        features = X.columns[mask]

        if name == "Logistic Regression":
            importance = np.abs(model.named_steps["model"].coef_[0])
        else:
            importance = model.named_steps["model"].feature_importances_

        ranking = pd.DataFrame(
            {"feature": features, "importance": importance}
        ).sort_values("importance", ascending=False)

        for rank, row in enumerate(ranking.head(20).itertuples(index=False), start=1):
            feature_rows.append(
                {
                    "model": name,
                    "rank": rank,
                    "probe_id": row.feature,
                    "importance": row.importance,
                }
            )

    pd.DataFrame(feature_rows).to_csv(
        RESULTS / "feature_ranking.tsv", sep="\t", index=False
    )

    # Compact performance figure.
    plot = metrics.set_index("model")[["roc_auc", "average_precision"]]
    ax = plot.plot(kind="bar", figsize=(7, 5))
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title("Project 05 — Cross-validated classification")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(FIGURES / "model_performance.png", dpi=160)
    plt.close()

    # ROC curves from out-of-fold predictions.
    fig, ax = plt.subplots(figsize=(7, 5))
    from sklearn.metrics import RocCurveDisplay
    for name, result in evaluations.items():
        RocCurveDisplay.from_predictions(
            y, result["probabilities"], name=f"{name} (AUC={result['roc_auc']:.3f})", ax=ax
        )
    ax.set_title("Project 05 — Out-of-fold ROC curves")
    plt.tight_layout()
    plt.savefig(FIGURES / "roc_curves.png", dpi=160)
    plt.close()

    report = f"""# Project 05 Results

## Dataset

- GEO accession: GSE42568
- Samples: {len(y)}
- Normal: {int((y == 0).sum())}
- Breast cancer: {int((y == 1).sum())}
- Features after zero-variance filtering: {X.shape[1]}
- Cross-validation: stratified 5-fold, shuffle=True, random_state=42
- Feature selection: top {k} ANOVA F-score features, learned within each training fold

## Cross-validated performance

| Model | ROC-AUC | Average Precision | Accuracy | Balanced Accuracy |
|---|---:|---:|---:|---:|
"""
    for row in metric_rows:
        report += (
            f"| {row['model']} | {row['roc_auc']:.4f} | "
            f"{row['average_precision']:.4f} | {row['accuracy']:.4f} | "
            f"{row['balanced_accuracy']:.4f} |\n"
        )

    report += """
## Interpretation

The reported metrics are out-of-fold predictions and therefore are not based on predictions from models trained on the corresponding test folds.

The feature ranking is exploratory because the final ranking models are fit on all samples after cross-validation. It should not be interpreted as an independently validated biomarker list.

The task is tissue-class classification within GSE42568. It is not a clinical diagnostic validation study.
"""
    (RESULTS / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
