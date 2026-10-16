#!/usr/bin/env python3
"""Validate the expected 10x Genomics filtered feature-barcode matrix files."""
import argparse
import sys
from pathlib import Path

MATRIX = ("matrix.mtx", "matrix.mtx.gz")
BARCODES = ("barcodes.tsv", "barcodes.tsv.gz")
FEATURES = ("features.tsv", "features.tsv.gz", "genes.tsv", "genes.tsv.gz")


def validate(directory: Path) -> list[str]:
    if not directory.is_dir():
        return [f"Input directory does not exist: {directory}"]
    errors = []
    for label, candidates in (
        ("matrix", MATRIX), ("barcodes", BARCODES), ("features/genes", FEATURES)
    ):
        if not any((directory / name).is_file() for name in candidates):
            errors.append(f"Missing {label} file; expected one of: {', '.join(candidates)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/raw/filtered_gene_bc_matrices/hg19"))
    args = parser.parse_args()
    errors = validate(args.input)
    if errors:
        print("INPUT VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(" - " + error, file=sys.stderr)
        return 1
    print(f"PASS: expected 10x matrix files found in {args.input}")
    print("NOTE: file presence only; matrix contents and biological quality are not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
