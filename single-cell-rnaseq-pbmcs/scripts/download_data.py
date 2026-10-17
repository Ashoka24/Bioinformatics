#!/usr/bin/env python3
"""Download and safely extract the public 10x PBMC 3k matrix archive."""
import shutil
import tarfile
import urllib.error
import urllib.request
from pathlib import Path

DATASET_PAGE = "https://www.10xgenomics.com/datasets/3-k-pbm-cells-from-a-healthy-donor-1-standard-1-1-0"
ARCHIVE_URL = "https://cf.10xgenomics.com/samples/cell-exp/1.1.0/pbmc3k/pbmc3k_filtered_gene_bc_matrices.tar.gz"
DEST = Path("data/raw")
ARCHIVE = DEST / "pbmc3k_filtered_gene_bc_matrices.tar.gz"


def safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.getmembers():
        target = (destination / member.name).resolve()
        if target != root and root not in target.parents:
            raise ValueError(f"Unsafe archive path: {member.name}")
    archive.extractall(destination, filter="data")


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE.exists():
        request = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "BioinformaticsPortfolio/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response, ARCHIVE.open("wb") as output:
                shutil.copyfileobj(response, output)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            ARCHIVE.unlink(missing_ok=True)
            raise SystemExit(f"Download failed: {exc}. Verify the archive from: {DATASET_PAGE}")
    try:
        with tarfile.open(ARCHIVE, "r:gz") as archive:
            safe_extract(archive, DEST)
    except (tarfile.TarError, OSError, ValueError) as exc:
        raise SystemExit(f"Archive extraction failed: {exc}")
    print(f"Extracted archive under {DEST}")
    print(f"Dataset provenance: {DATASET_PAGE}")
    print("Next, locate the extracted matrix directory and run scripts/validate_inputs.py --input <directory>.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
