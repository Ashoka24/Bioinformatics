# Completed WES Run — HCC1395

## Execution summary

A local whole-exome sequencing workflow was completed with **nf-core/sarek 3.10.0**, Nextflow, and Docker. The final Nextflow session status was `OK`.

- Analysis: matched tumor/normal somatic variant analysis
- Pair label in output: `HCC1395_vs_HCC1395BL`
- Reference: GATK GRCh38
- Variant caller: Mutect2
- Annotation: Ensembl VEP
- Requested tools: `mutect2,vep`
- Workflow output directory: `results/hcc1395_sarek/`

## Validated output

Final annotated VCF:

`annotation/mutect2/HCC1395_vs_HCC1395BL/HCC1395_vs_HCC1395BL.mutect2.filtered_VEP.ann.vcf.gz`

- Compressed VCF size: approximately 1.26 MB
- VCF records reported by `bcftools view -H`: **5,289**
- VEP `CSQ` annotation header: present
- `gzip -t` integrity check: passed
- Tabix index file (`.tbi`): present, approximately 50 KB
- MultiQC HTML report: `multiqc/multiqc_report.html`, approximately 2.81 MB

The VCF index file was present, but index-query validation was not independently completed in the recorded checks.

## Reproducibility notes

The local run used a low-memory Nextflow configuration at `/home/ashoka/sarek-config/lowmem.config` and a parameters file at `config/sarek_params.json`. The absolute path is specific to the execution machine; do not rely on it for another installation. Use a portable, documented configuration when reproducing the run.

Raw FASTQ/SRA data, reference assets, Nextflow work directories, Docker storage, and temporary files should remain outside GitHub. Keep only code, reusable configuration templates, concise reports, and small non-sensitive QC summaries in version control. Do not commit credentials or machine-specific paths.

## Interpretation

These are workflow-level validation results, not clinical conclusions. A count of VCF records is not equivalent to a count of clinically significant mutations. Any biological interpretation requires review of filtering, annotation, sample provenance, and relevant quality metrics.
