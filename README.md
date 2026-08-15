# Bioinformatics
Bioinformatics portfolio featuring NGS data analysis, genomics, transcriptomics, metagenomics, microbiome analysis, Python/R, Linux, and reproducible bioinformatics pipelines.
# Metagenomics
                 RAW FASTQ
                    │
          ┌─────────┴─────────┐
          │                   │
     ILLUMINA PE          NANOPORE
       R1 + R2              FASTQ
          │                   │
       FastQC              NanoPlot
          │                   │
       MultiQC          NanoFilt/Filtlong
          │                   │
        fastp             Filtering
          │                   │
          └─────────┬─────────┘
                    │
             Optional Host
                Removal
                    │
                    ▼
          ┌───────────────────┐
          │ TAXONOMIC PROFILING│
          └───────────────────┘
             │       │       │
          Kraken2 Centrifuge MetaPhlAn*
             │       │       │
             └───────┴───────┘
                    │
                    ▼
          FUNCTIONAL PROFILING*
                    │
                 HUMAnN
                    │
                    ▼
          VISUALIZATION
                    │
                    ▼
        BIOLOGICAL INTERPRETATION
