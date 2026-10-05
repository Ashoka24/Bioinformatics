# Actual outcome — SRR26534086

Results generated from the public FASTQ; no private/company data. Single-run workflow validation, not cohort-level inference.

## Dataset
- BioSample: `SAMN37943185`
- BioProject: `PRJNA1031545`
- Experiment: `SRX22237515`
- Assay: 16S rRNA V3–V4
- Instrument: Illumina MiSeq

## Processing
- QIIME 2 2024.10 amplicon Docker image
- Cutadapt primer trimming with the study-reported V3–V4 primers
- DADA2 paired-end; truncation 280/260; max EE 2/2
- SILVA 138 99% full-length Naive Bayes classifier
- Classifier SHA256: `c08a1aa4d56b449b511f7215543a43249ae9c54b57491428a7e5548a62613616`

## Actual metrics
- Input/denoised table read count: **23,370**
- Observed ASVs: **184**
- Shannon: **4.081720**
- Simpson: **0.966501**
- Inverse Simpson: **29.851448**
- Pielou evenness: **0.782698**
- QIIME observed_features: **184**
- QIIME Shannon: **5.888677757837011**

## Taxonomy outputs
Phylum, class, order, family, genus and species abundance tables are generated from the ASV counts and assigned taxonomy.

Beta diversity/PERMANOVA is intentionally omitted because only one sample is analyzed.
