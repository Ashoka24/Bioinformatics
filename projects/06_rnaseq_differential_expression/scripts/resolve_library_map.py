#!/usr/bin/env python3
import pandas as pd
from pysradb.sraweb import SRAweb

GSM = [
"GSM3211196","GSM3211194","GSM3211169","GSM3211171","GSM3211174","GSM3211175",
"GSM3211177","GSM3211178","GSM3211186","GSM3211185","GSM3211180","GSM3211179",
"GSM3211183","GSM3211182","GSM3211189","GSM3211190","GSM3211193","GSM3211191"
]

db = SRAweb()
df = db.sra_metadata("SRP151065", detailed=True)

if "experiment_geo_accession" not in df.columns:
    raise SystemExit("pysradb did not return experiment_geo_accession")

cols = [c for c in ["experiment_geo_accession", "library_name", "experiment_accession"] if c in df.columns]
m = df[cols].copy()
m = m[m["experiment_geo_accession"].isin(GSM)].drop_duplicates("experiment_geo_accession")

if len(m) != len(GSM):
    missing = sorted(set(GSM) - set(m["experiment_geo_accession"]))
    raise SystemExit("Missing GSM mappings: " + ",".join(missing))

m[["experiment_geo_accession", "library_name"]].to_csv(
    "results/library_mapping.tsv", sep="\t", index=False
)
