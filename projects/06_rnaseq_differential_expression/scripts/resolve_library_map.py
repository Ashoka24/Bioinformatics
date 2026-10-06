#!/usr/bin/env python3
import pandas as pd

gsm = ["GSM3211169","GSM3211170","GSM3211171","GSM3211172","GSM3211173","GSM3211174","GSM3211175","GSM3211176","GSM3211177","GSM3211178","GSM3211179","GSM3211180","GSM3211181","GSM3211182","GSM3211183","GSM3211184","GSM3211185","GSM3211186","GSM3211187","GSM3211188","GSM3211189","GSM3211190","GSM3211191","GSM3211192","GSM3211193","GSM3211194","GSM3211195","GSM3211196"]
libraries = ["lib10819","lib10820","lib10821","lib10823","lib11819","lib11820","lib11821","lib11822","lib11823","lib11824","lib12778","lib12779","lib12780","lib12783","lib12784","lib12785","lib12786","lib12787","lib12788","lib12791","lib12792","lib12793","lib12794","lib12795","lib12796","lib7438","lib7439","lib7440"]

if len(gsm) != 28 or len(libraries) != 28:
    raise SystemExit("GEO sample count and matrix library count must both equal 28")

pd.DataFrame({"gsm": gsm, "library_name": libraries}).to_csv("results/library_mapping.tsv", sep="\t", index=False)
