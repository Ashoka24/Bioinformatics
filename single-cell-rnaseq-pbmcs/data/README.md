# Data provenance and storage policy

Dataset: 10x Genomics, 3k PBMCs from a Healthy Donor.

Official source: https://www.10xgenomics.com/datasets/3-k-pbm-cells-from-a-healthy-donor-1-standard-1-1-0

Run python scripts/download_data.py to download and extract the filtered feature-barcode matrix. Files are stored under data/raw/, which is ignored by Git. Do not commit downloaded matrices, derived AnnData objects, or generated results.

Expected files include matrix.mtx or matrix.mtx.gz, barcodes.tsv or barcodes.tsv.gz, and genes.tsv/features.tsv or their compressed variants.
