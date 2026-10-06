# Dataset provenance

## Source

NCBI BioProject: PRJNA786061

Study: Association between anemia and gut microbiome composition in the rural Odisha population.

NCBI lists 102 SRA experiments and approximately 3.1 GB of sequence data for this metagenome project.

## Selection policy

At runtime the workflow queries the public ENA run API for PRJNA786061 and selects a paired-end WGS run with available FASTQ files. The exact run accession is written to results/run_metadata.tsv.

## Analysis scope

Only the selected run is analyzed in this portfolio project. The source project contains 102 samples, but this workflow is intentionally limited to one sample so the complete pipeline can run within ordinary CI compute constraints.

No cohort-level anemia comparison is performed.
