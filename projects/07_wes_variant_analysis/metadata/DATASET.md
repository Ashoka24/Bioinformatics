# Dataset — Project 07 WES

## Input

The workflow is designed for paired-end human whole-exome sequencing FASTQ files.

Human sequencing reads are not stored in the repository. Input files are supplied through an approved public dataset or authorized study and referenced in `config/samplesheet.csv`.

## Sample sheet

| sample_id | fastq_1 | fastq_2 |
|---|---|---|
| SAMPLE01 | /data/SAMPLE01_R1.fastq.gz | /data/SAMPLE01_R2.fastq.gz |

S3 URIs are also supported.

## Reference requirements

The reference genome and GATK resource bundle must be recorded before a production run. The same reference build must be used for alignment, variant calling and annotation.

## Scope

The initial portfolio implementation focuses on germline SNV/indel processing. Copy-number analysis, structural variants and clinical interpretation are outside the initial scope.
