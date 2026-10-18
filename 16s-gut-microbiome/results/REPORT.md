# Actual outcome — SRR26534086

Results generated from one public NCBI SRA run. This is a workflow demonstration, not a cohort-level or clinical analysis.

## Dataset
- BioSample: `SAMN37943185`
- BioProject: `PRJNA1031545`
- Experiment: `SRX22237515`
- Assay: 16S rRNA V3–V4 amplicon
- Instrument: Illumina MiSeq

## Processing
- QIIME 2 amplicon Docker image: `2024.10`
- Primer trimming with QIIME 2 Cutadapt using the documented V3–V4 primers
- Denoising: QIIME 2 Deblur `denoise-16S`, trim length 200 bp
- Taxonomy: SILVA 138 99% Naive Bayes classifier
- Classifier SHA-256: `c08a1aa4d56b449b511f7215543a43249ae9c54b57491428a7e5548a62613616`

This result was produced by the Deblur workflow above. It should not be described as a DADA2 run or as using the separate nf-core/ampliseq truncation settings.

## Results
- Reads represented in the exported feature table: **23,370**
- Observed features: **184**
- Shannon diversity (natural logarithm, calculated from feature counts): **4.081720**
- Simpson diversity (1 − sum of squared proportions): **0.966501**
- Inverse Simpson diversity: **29.851448**
- Pielou evenness: **0.782698**
- QIIME 2 observed features: **184**
- QIIME 2 Shannon entropy (base 2): **5.888677757837011**

The two Shannon values use different logarithm bases: the value calculated here uses the natural logarithm, while the QIIME 2 output uses base 2. They describe the same feature-count distribution and should not be compared without accounting for that difference.

## Taxonomy outputs
Phylum-, class-, order-, family-, genus-, and species-level abundance tables were generated from the feature counts and assigned taxonomy. Taxonomic assignments remain dependent on the reference classifier and should be interpreted accordingly.

Beta diversity and PERMANOVA are omitted because this analysis contains only one sample.
