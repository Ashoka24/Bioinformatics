# Dataset provenance

## Source

NCBI BioProject: PRJNA273761

Study: Metagenomes from human infant fecal samples with and without necrotizing enterocolitis.

Selected run: SRR1779146  
Sample: SAMN03295851  
Experiment: SRX858749  
Study accession: SRP052967

NCBI lists this as paired-end Illumina HiSeq 2000 whole-genome shotgun metagenomic data from human gut. See the [NCBI SRA run record](https://www.ncbi.nlm.nih.gov/sra/SRR1779146) and [ENA run record](https://www.ebi.ac.uk/ena/browser/view/SRR1779146) for current run metadata.

## Selection policy

A fixed public run is used so the analysis is deterministic and reproducible. The workflow records the accession and sequencing metadata in `results/run_metadata.tsv`.

## Analysis scope

Only SRR1779146 is analyzed in this portfolio project. The broader study is available under [BioProject PRJNA273761](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA273761). This workflow intentionally analyzes one public paired-end WGS sample so the complete Kraken2 + Centrifuge workflow can run within ordinary CI compute constraints.

No cohort-level NEC comparison is performed.
