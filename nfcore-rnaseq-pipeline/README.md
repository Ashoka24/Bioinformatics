# Reproducible RNA-seq Pipeline with nf-core and Nextflow

## Overview figure

![nf-core RNA-seq validation overview](figures/03_overview.svg)
I use the nf-core/rnaseq test profile to check that Nextflow, Docker and the pipeline work together in a repeatable run. This is a pipeline test, not a biological analysis of a study cohort.

## What I tested

Run the nf-core/rnaseq test profile in Docker and verify the run through GitHub Actions.

This repository focuses on running and validating the nf-core workflow. The separate RNA-seq differential-expression analysis covers the biological comparison.

## Workflow figure

![Project 04 workflow](figures/01_workflow.svg)

## Workflow

nf-core/rnaseq test data → Nextflow → Docker containers → QC → trimming → strandedness inference → alignment / quantification → expression outputs + QC reports → GitHub Actions validation

## Reproducibility target

- nf-core/rnaseq: 3.27.0
- Execution engine: Nextflow 26.04.6 in CI
- Container runtime: Docker
- Validation: GitHub Actions
- Test profile: test,docker
- Output directory: results

## Execution evidence

The figure summarizes the successful GitHub Actions run recorded below. It is an execution-status summary, not a sequencing QC plot.

![nf-core execution evidence](figures/04_ci_evidence.svg)

## CI verification

The GitHub Actions test run completed successfully on 6 October 2026.

- Workflow run: [#37505789353](https://github.com/Ashoka24/Bioinformatics/actions/runs/37505789353)
- Commit: ce80a170070b3fda3ce377dea07b4aae443e3488
- Job: nfcore-test
- Job conclusion: success
- nf-core/rnaseq test step: success
- Output artifact: project04-nfcore-results
- Artifact size: 50,007,842 bytes
- Artifact SHA-256: 343073a039e4408d5f710e30592294c1c6c30b9faa84881dfb0e94668da1855d
- Artifact contains the CI results/ output and .nextflow.log.

The first CI attempt failed during parameter validation because outdir was required. The workflow was corrected to pass --outdir results, then the complete nf-core test succeeded.

## Output map

![Project 04 output map](figures/02_output_file_map.svg)

## Run locally

    nextflow run nf-core/rnaseq -r 3.27.0 -profile test,docker --outdir results

For repeated execution, Nextflow supports -resume so completed processes can be reused when inputs and process definitions are unchanged.

    nextflow run nf-core/rnaseq -r 3.27.0 -profile test,docker --outdir results -resume

## Repository layout

    nfcore-rnaseq-pipeline/
    ├── README.md
    ├── params/
    │   └── test.yml
    ├── scripts/
    │   └── run_test.sh
    └── figures/
        ├── 01_workflow.svg
        └── 02_output_file_map.svg

The CI workflow lives at .github/workflows/project04_nfcore.yml.

## Scope boundary

This project validates pipeline execution and reproducibility. It does not make biological claims from the nf-core test dataset and does not substitute for the cohort-level RNA-seq analysis planned as Project 06.
