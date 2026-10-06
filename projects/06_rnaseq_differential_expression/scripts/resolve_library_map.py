#!/usr/bin/env python3
import re
import pandas as pd
from pysradb.sraweb import SRAweb

LIBS = [
"lib10819","lib10820","lib10821","lib10823","lib11819","lib11820","lib11821",
"lib11822","lib11823","lib11824","lib12778","lib12779","lib12780","lib12783",
"lib12784","lib12785","lib12786","lib12787","lib12788","lib12791","lib12792",
"lib12793","lib12794","lib12795","lib12796","lib7438","lib7439","lib7440"
]

db = SRAweb()
query = " OR ".join([f'"{x}"' for x in LIBS])
hits = db.search_sra(search_str=query)

if hits is None or hits.empty:
    raise SystemExit("SRA search returned no library records")

hits = hits[hits["library_name"].isin(LIBS)].copy()

def find_gsm(row):
    for value in row.astype(str).tolist():
        m = re.search(r"GSM\d+", value)
        if m:
            return m.group(0)
    return None

hits["gsm"] = hits.apply(find_gsm, axis=1)
m = hits[["gsm", "library_name"]].dropna().drop_duplicates("gsm")

expected = set([
"GSM3211196","GSM3211194","GSM3211169","GSM3211171","GSM3211174","GSM3211175",
"GSM3211177","GSM3211178","GSM3211186","GSM3211185","GSM3211180","GSM3211179",
"GSM3211183","GSM3211182","GSM3211189","GSM3211190","GSM3211193","GSM3211191"
])

m = m[m["gsm"].isin(expected)]
if len(m) != len(expected):
    print(hits[["experiment_accession","experiment_title","sample_accession","sample_title","library_name","gsm"]].to_string(index=False))
    raise SystemExit("Incomplete GSM/library mapping")

m.to_csv("results/library_mapping.tsv", sep="\t", index=False)
