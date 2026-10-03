# Downstream 16S Analysis

## Technical validation

The first NCBI run is a pipeline-validation experiment:

Raw FASTQ → FastQC/MultiQC → Ampliseq → ASVs + taxonomy → descriptive alpha diversity.

## Cohort experiment

After multiple biologically independent samples are available:

ASV table → filtering/QC → relative abundance → alpha diversity + Bray–Curtis + PCoA + taxa composition → statistical model → biological interpretation.

### Shannon diversity

    qiime diversity alpha \
      --i-table feature-table.qza \
      --p-metric shannon \
      --o-alpha-diversity shannon.qza

### Observed ASVs

    qiime diversity alpha \
      --i-table feature-table.qza \
      --p-metric observed_features \
      --o-alpha-diversity observed_features.qza

### Bray–Curtis

Only after multiple samples:

    qiime diversity beta \
      --i-table feature-table.qza \
      --p-metric braycurtis \
      --o-distance-matrix bray_curtis.qza

### PCoA

    qiime diversity pcoa \
      --i-distance-matrix bray_curtis.qza \
      --o-pcoa bray_curtis_pcoa.qza

### Interactive PCoA

    qiime emperor plot \
      --i-pcoa bray_curtis_pcoa.qza \
      --m-metadata-file sample-metadata.tsv \
      --o-visualization bray_curtis_emperor.qzv

### Taxa bar plot

    qiime taxa barplot \
      --i-table feature-table.qza \
      --i-taxonomy taxonomy.qza \
      --m-metadata-file sample-metadata.tsv \
      --o-visualization taxa_barplot.qzv

## Statistical analysis

Do not run a disease-vs-control test on the single technical-validation sample.

For the cohort experiment, define the biological contrast from study metadata before looking at taxonomic differences.

Possible analyses:

- alpha diversity: appropriate parametric/non-parametric test or linear model;
- beta diversity: PERMANOVA with pre-specified covariates;
- differential abundance: ANCOM-BC/ANCOM-BC2 or another compositional method;
- multiple testing correction: FDR.

Longitudinal or paired data require subject-aware models rather than treating every sample as independent.

## Biological interpretation

A strong interpretation has four layers:

1. Observation — what changed?
2. Statistical evidence — how strong is the evidence?
3. Biological plausibility — is the organism/function relevant?
4. Limitation — what alternative explanations remain?

Avoid causal statements from observational 16S data.
