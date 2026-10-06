# Dataset provenance

## Source

NCBI BioProject: PRJNA273761

Study: Metagenomes from human infant fecal samples with and without necrotizing enterocolitis.

Selected run: SRR1779146  
Sample: SAMN03295851  
Experiment: SRX858749  
Study accession: SRP052967

NCBI identifies the selected experiment as human gut metagenome, Illumina HiSeq 2000, WGS, metagenomic source, paired-end, with 8M spots, 2.3G bases and approximately 1.5 GB download size. citeturn8search1

## Selection policy

A fixed public run is used so the analysis is deterministic and reproducible. The workflow records the accession and sequencing metadata in `results/run_metadata.tsv`.

## Analysis scope

Only SRR1779146 is analyzed in this portfolio project. The source BioProject contains 60 SRA experiments; this workflow intentionally analyzes one public paired-end WGS sample so the complete Kraken2 + Centrifuge workflow can run within ordinary CI compute constraints. citeturn6search0

No cohort-level NEC comparison is performed.
