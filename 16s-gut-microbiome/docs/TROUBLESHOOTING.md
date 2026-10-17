# Troubleshooting — Project 01

This project is designed to preserve real execution decisions rather than hide failures. Record important failures and fixes in `logs/RESOURCE_NOTES.md`.

## SRA download

### `prefetch: command not found`

Install the NCBI SRA Toolkit in the WSL environment and rerun:

```bash
bash scripts/00_setup.sh
```

Do not replace the accession with an invented local filename.

### TLS / certificate errors

If `prefetch` reports certificate or TLS failures, verify that WSL has working network access and current CA certificates. Re-run `vdb-validate` after a successful download.

## FastQC / MultiQC

### No FASTQ files found

Confirm the download step completed:

```bash
ls -lh /mnt/c/Users/ashok/OneDrive/Desktop/Ashoka/data/16s_ncbi_gut/RawData/SRR26534086/fastq/
```

Expected paired files are:

```text
SRR26534086_1.fastq.gz
SRR26534086_2.fastq.gz
```

### FastQC Java error

If FastQC reports a Java class-file/runtime mismatch, check:

```bash
java -version
fastqc --version
```

The Java runtime must be compatible with the installed FastQC build. Fix the environment before interpreting QC.

## Docker

### Docker daemon is not running

Check:

```bash
docker info
```

If the client works but the daemon is unavailable, start/fix Docker according to the Docker installation used by the WSL environment. Then verify `docker info` succeeds before starting nf-core/ampliseq.

### Permission denied on the Docker socket

Check:

```bash
groups
docker info
```

Resolve the local Docker group/daemon permission problem rather than running the entire workflow as root.

## Nextflow / nf-core/ampliseq

### Process requirement exceeds available memory

This is a resource constraint, not a biological failure. Record:

- requested memory;
- available memory;
- process name;
- host/VM memory;
- the parameter change used to retry.

For example, a DADA2 step requesting 42 GB cannot execute on a WSL VM with only about 12 GB available. Increase the VM/WSL memory or reduce the workflow resource requirement only when scientifically and computationally appropriate.

### Pipeline resumes after a failure

The execution script uses:

```text
-resume
```

This is intentional. Keep the same work directory when retrying so completed processes can be reused.

## Paired-read validation

If R1 and R2 read counts differ, stop. Do not continue into taxonomic analysis until the FASTQ files are repaired or re-downloaded.

## Interpretation rule

A successful software run does not automatically mean a valid biological conclusion. Separate:

1. technical QC;
2. feature/taxonomy generation;
3. statistical evidence;
4. biological interpretation;
5. limitations.
