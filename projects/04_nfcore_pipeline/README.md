# Project 04 — Production-style Nextflow / nf-core RNA-seq Pipeline

A workflow-engineering project focused on reproducibility, containerization, parameterization, resource awareness and automated validation using Nextflow and nf-core.

## Objective

Validate a complete RNA-seq workflow reproducibly in Docker using the maintained nf-core/rnaseq test profile and GitHub Actions.

This project is intentionally different from Project 06: Project 04 focuses on workflow engineering and execution reliability; Project 06 will focus on biological transcriptomics analysis and differential expression.

## Workflow

nf-core/rnaseq test data → Nextflow → Docker containers → QC → trimming → strandedness inference → alignment / quantification → expression outputs + QC reports → GitHub Actions validation

## Reproducibility target

- nf-core/rnaseq: 3.27.0
- Execution engine: Nextflow
- Container runtime: Docker
- Validation: GitHub Actions
- Test profile: test,docker

The nf-core documentation recommends Docker or Singularity for reproducible execution and provides a test profile for automated testing. citeturn1search1turn1search0

## Run locally

    nextflow run nf-core/rnaseq -r 3.27.0 -profile test,docker

For repeated execution, Nextflow supports -resume so completed processes can be reused when inputs and process definitions are unchanged. citeturn1search0

    nextflow run nf-core/rnaseq -r 3.27.0 -profile test,docker -resume

## Repository layout

    04_nfcore_pipeline/
    ├── README.md
    ├── params/
    │   └── test.yml
    ├── scripts/
    │   └── run_test.sh
    └── figures/
        └── 01_workflow.svg

The CI workflow lives at .github/workflows/project04_nfcore.yml.

## Verification

The project is not marked complete until the GitHub Actions run succeeds. The final README will record actual run status and verified outputs rather than estimated metrics.

## Scope boundary

This project validates pipeline execution and reproducibility. It does not make biological claims from the nf-core test dataset and does not substitute for the cohort-level RNA-seq analysis planned as Project 06.
