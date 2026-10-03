# Workflow notes

The supplied 16S workflow uses a practical sequence: raw FASTQ collection, FastQC/MultiQC, file preparation, nf-core/ampliseq with Docker, then downstream QIIME 2 analysis. It documents V3–V4 primers, truncation 280/260, SILVA taxonomy, DADA2-related settings and resource limits.

This portfolio version keeps that analysis logic but replaces private/vendor data with the public NCBI run SRR26534086.

## Provenance

NCBI SRA → SRX22237515 → SAMN37943185 → SRR26534086

The run is paired-end Illumina MiSeq 16S amplicon data from human stool.

## QC before trimming

The documented 280/260 truncation values are retained as a reproducibility reference. They should not be copied blindly to another sequencing run. Inspect FastQC/MultiQC first and document any parameter change.

## Reproducibility

Git stores accession IDs, metadata, parameters, scripts, documentation and resource notes. FASTQ/SRA files, generated QIIME 2 artifacts and Nextflow work directories stay outside Git.
