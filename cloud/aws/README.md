# AWS Execution

This directory contains the shared cloud execution pattern for the omics portfolio.

## Intended flow

1. GitHub contains versioned workflow code.
2. An EC2 instance is started with Docker, Nextflow and the AWS CLI.
3. An IAM role provides only the required S3 permissions.
4. Input FASTQ/count data is staged from S3.
5. The project workflow runs locally on the EC2 instance.
6. Results are synchronized back to S3.
7. Logs and lightweight summaries remain available through GitHub and workflow artifacts.

## Required environment

- AWS CLI
- Nextflow
- Docker
- Java for Nextflow
- project-specific reference data

The runner deliberately does not contain AWS access keys. Authentication is expected through the instance role or another approved AWS identity mechanism.

## Cost control

Use small test datasets first, stop EC2 instances when jobs finish, and keep large generated files in S3 rather than Git.
