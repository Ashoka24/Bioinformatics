# Data Provenance — Project 01

## Public source

The workflow is based on the public NCBI SRA accession:

```text
SRR26534086
```

Associated identifiers:

| Level | Accession |
|---|---|
| SRA run | SRR26534086 |
| BioSample | SAMN37943185 |
| BioProject | PRJNA1031545 |
| Experiment | SRX22237515 |

## Sequencing design

The selected run is documented as:

- human stool;
- 16S rRNA amplicon;
- V3–V4 region;
- Illumina MiSeq;
- paired-end.

The documented primer sequences are:

```text
Forward: CCTACGGGNGGCWGCAG
Reverse: GACTACHVGGGTATCTAATCC
```

## Scope

The selected run is a workflow-validation dataset. One run is sufficient to demonstrate the computational path from public sequence data to QC and downstream feature/taxonomy processing, but it is not sufficient for disease-vs-control inference or differential abundance testing.

The parent BioProject can be expanded later after the run metadata have been retrieved and inspected.

## Provenance chain

```text
NCBI SRA
  |
  +-- BioProject: PRJNA1031545
        |
        +-- Experiment: SRX22237515
              |
              +-- BioSample: SAMN37943185
                    |
                    +-- Run: SRR26534086
```

## Repository boundary

The repository stores accession identifiers, metadata definitions, scripts, parameters and documentation.

The repository does **not** store:

- raw FASTQ files;
- SRA files;
- QIIME 2 artifacts;
- Nextflow work directories;
- private/company sequencing data;
- generated results that have not actually been produced.

This separation keeps the public portfolio reproducible without exposing restricted data.
