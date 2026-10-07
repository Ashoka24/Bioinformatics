# AWS Omics Execution Architecture

The portfolio uses one common cloud pattern so the WES, RNA-seq, single-cell, miRNA-seq and methylation projects can move from a workstation to AWS without redesigning the analysis.

## Common flow

S3 input data → EC2 or compatible compute → Docker / Nextflow → project workflow → results → S3

## Repository-to-cloud mapping

| Layer | Portfolio implementation |
|---|---|
| Storage | Amazon S3 |
| Compute | EC2 initially; HPC/SLURM-compatible later |
| Workflow | Nextflow / nf-core |
| Containers | Docker |
| Code | GitHub |
| Automation | GitHub Actions |
| Analysis | Python, R, Bash |
| Results | S3 + workflow artifacts |

## S3 layout

```text
s3://bioinformatics-portfolio/
├── raw/{wes,rnaseq,scrnaseq,mirnaseq,methylation}/
├── reference/
└── results/{wes,rnaseq,scrnaseq,mirnaseq,methylation}/
```

Raw sequencing data is not committed to GitHub. The repository stores code, metadata, workflow definitions, documentation and lightweight example outputs.

## Security and reproducibility

AWS credentials must never be committed. Compute instances should use IAM roles with the minimum S3 permissions required. Every run should record the accession or input source, reference build, container version and workflow revision.

The goal is a realistic cloud-ready bioinformatics workflow without unnecessary AWS cost.
