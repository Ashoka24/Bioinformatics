#!/usr/bin/env python3
"""Reproducible downstream analysis of a small 16S feature-table excerpt."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "results"
OUT.mkdir(exist_ok=True)

table = pd.read_csv(DATA / "feature-table.tsv", sep="\t", index_col=0)
metadata = pd.read_csv(DATA / "sample-metadata.tsv", sep="\t")

relative = table.div(table.sum(axis=0), axis=1)
shannon = -(relative.replace(0, np.nan) * np.log(relative.replace(0, np.nan))).sum(axis=0)

summary = pd.DataFrame({
    "sample_id": table.columns,
    "total_reads": table.sum(axis=0).values,
    "observed_features": (table > 0).sum(axis=0).values,
    "shannon": shannon.values,
})
summary.to_csv(OUT / "sample_summary.csv", index=False)

relative.mean(axis=1).sort_values(ascending=False).rename(
    "mean_relative_abundance"
).reset_index().to_csv(OUT / "top_features.csv", index=False)

distance = squareform(pdist(relative.T.values, metric="braycurtis"))
n = len(table.columns)
centering = np.eye(n) - np.ones((n, n)) / n
gram = -0.5 * centering @ (distance ** 2) @ centering
eigenvalues, eigenvectors = eigh(gram)
order = np.argsort(eigenvalues)[::-1]
eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
coordinates = eigenvectors[:, :2] * np.sqrt(np.maximum(eigenvalues[:2], 0))

pcoa = pd.DataFrame({
    "sample_id": table.columns,
    "PCoA1": coordinates[:, 0],
    "PCoA2": coordinates[:, 1],
}).merge(
    metadata[["sample-id", "subject", "reported-antibiotic-usage"]],
    left_on="sample_id", right_on="sample-id"
).drop(columns="sample-id")
pcoa.to_csv(OUT / "bray_curtis_pcoa.csv", index=False)

print("Analysis complete.")
print(summary.to_string(index=False))
