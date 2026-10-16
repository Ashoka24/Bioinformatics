#!/usr/bin/env python3
"""Validate the Project 07 nf-core/sarek tumor-normal samplesheet."""

import argparse
import csv
import gzip
import sys
from pathlib import Path

REQUIRED_COLUMNS = ["patient", "sample", "lane", "fastq_1", "fastq_2", "status"]
EXPECTED_SAMPLES = {"HCC1395BL": "0", "HCC1395": "1"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check samplesheet columns, sample pairing, FASTQ paths and optional gzip integrity."
    )
    parser.add_argument(
        "--samplesheet",
        default="config/samplesheet.csv",
        help="Samplesheet path, relative to the project directory unless absolute.",
    )
    parser.add_argument(
        "--check-files",
        action="store_true",
        help="Require FASTQs to exist and read each gzip stream to EOF to verify integrity.",
    )
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parents[1]
    sheet_path = Path(args.samplesheet)
    if not sheet_path.is_absolute() and not sheet_path.is_file():
        sheet_path = project_dir / sheet_path

    if not sheet_path.is_file():
        print(f"ERROR: samplesheet not found: {sheet_path}", file=sys.stderr)
        return 1

    try:
        with sheet_path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            columns = reader.fieldnames or []
            missing = [column for column in REQUIRED_COLUMNS if column not in columns]
            if missing:
                print(f"ERROR: missing required columns: {', '.join(missing)}", file=sys.stderr)
                return 1
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        print(f"ERROR: could not read samplesheet: {exc}", file=sys.stderr)
        return 1

    if not rows:
        print("ERROR: samplesheet has no sample rows.", file=sys.stderr)
        return 1

    errors = []
    seen = set()
    patient_statuses = {}
    sample_statuses = {}

    for line_number, row in enumerate(rows, start=2):
        values = {key: (row.get(key) or "").strip() for key in REQUIRED_COLUMNS}
        if any(not values[key] for key in REQUIRED_COLUMNS):
            errors.append(f"line {line_number}: one or more required fields are blank")
            continue

        key = (values["patient"], values["sample"], values["lane"])
        if key in seen:
            errors.append(f"line {line_number}: duplicate patient/sample/lane entry {key}")
        seen.add(key)

        if values["status"] not in {"0", "1"}:
            errors.append(f"line {line_number}: status must be 0 (normal) or 1 (tumor)")
        patient_statuses.setdefault(values["patient"], []).append(values["status"])
        sample_statuses[values["sample"]] = values["status"]

        for column in ("fastq_1", "fastq_2"):
            fastq = Path(values[column])
            if not fastq.is_absolute():
                fastq = project_dir / fastq
            if args.check_files:
                if not fastq.is_file():
                    errors.append(f"line {line_number}: {column} file not found: {fastq}")
                elif not fastq.name.endswith(".fastq.gz"):
                    errors.append(f"line {line_number}: expected a .fastq.gz file: {fastq}")
                else:
                    try:
                        with gzip.open(fastq, "rb") as stream:
                            while stream.read(1024 * 1024):
                                pass
                    except (OSError, EOFError) as exc:
                        errors.append(f"line {line_number}: gzip integrity check failed for {fastq}: {exc}")

    for patient, statuses in patient_statuses.items():
        if statuses.count("0") != 1 or statuses.count("1") != 1:
            errors.append(
                f"patient {patient}: expected exactly one normal (status=0) and one tumor (status=1) row"
            )

    if len(patient_statuses) != 1 or "HCC1395" not in patient_statuses:
        errors.append("expected the HCC1395 matched tumor/normal pair under patient ID HCC1395")

    if sample_statuses.get("HCC1395BL") != "0":
        errors.append("HCC1395BL must be the normal sample (status=0)")
    if sample_statuses.get("HCC1395") != "1":
        errors.append("HCC1395 must be the tumor sample (status=1)")
    if set(sample_statuses) != set(EXPECTED_SAMPLES):
        errors.append("expected exactly the samples HCC1395BL and HCC1395")

    if errors:
        print("SAMPLESHEET VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"PASS: samplesheet structure and HCC1395 pairing validated ({len(rows)} rows).")
    if args.check_files:
        print("PASS: all paired FASTQ files exist and gzip integrity checks passed.")
    else:
        print("NOTE: FASTQ existence and gzip integrity were not checked; rerun with --check-files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
