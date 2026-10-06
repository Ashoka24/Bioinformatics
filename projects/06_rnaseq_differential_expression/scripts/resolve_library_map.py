#!/usr/bin/env python3
import pandas as pd
from pysradb.sraweb import SRAweb

GSM = [
"GSM3211196","GSM3211194","GSM3211169","GSM3211171","GSM3211174","GSM3211175",
"GSM3211177","GSM3211178","GSM3211186","GSM3211185","GSM3211180","GSM3211179",
"GSM3211183","GSM3211182","GSM3211189","GSM3211190","GSM3211193","GSM3211191"
]

db = SRAweb()

# GEO GSM -> SRA experiment (SRX)
gsm_srx = db.gsm_to_srx(GSM)
gsm_srx = gsm_srx[["experiment_alias", "experiment_accession"]].drop_duplicates()
gsm_srx = gsm_srx.rename(columns={"experiment_alias": "gsm"})

# SRA experiment -> internal library name
sra = db.sra_metadata("SRP151065", detailed=False)
sra = sra[["experiment_accession", "library_name"]].drop_duplicates()

m = gsm_srx.merge(sra, on="experiment_accession", how="left")
m = m[m["gsm"].isin(GSM)].drop_duplicates("gsm")

if len(m) != len(GSM) or m["library_name"].isna().any():
    missing = sorted(set(GSM) - set(m["gsm"]))
    if m["library_name"].isna().any():
        missing += m.loc[m["library_name"].isna(), "gsm"].tolist()
    raise SystemExit("Missing GSM/library mappings: " + ",".join(sorted(set(missing))))

m[["gsm", "library_name"]].to_csv(
    "results/library_mapping.tsv", sep="\t", index=False
)
