# Completed WES Run — HCC1395

## Execution summary

A local whole-exome sequencing workflow was completed with **nf-core/sarek 3.10.0**, Nextflow, and Docker. The final Nextflow session status was `OK`.

- Analysis: matched tumor/normal somatic variant analysis
- **Tumor sample ID:** `HCC1395` (`status=1` in the HCC1395 example samplesheet)
- **Normal sample ID:** `HCC1395BL` (`status=0` in the HCC1395 example samplesheet)
- Pair label in output: `HCC1395_vs_HCC1395BL`
- This report and its VCF describe the local HCC1395/HCC1395BL run, not the separate planned GSE179296 / Sample 1001 public pilot (`T1001` / `N1001`).
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

The local run used a low-memory Nextflow configuration specific to the execution machine; that local configuration is not included in this repository. The exact absolute path is intentionally omitted. Use a portable, documented configuration when reproducing the run.

Raw FASTQ/SRA data, reference assets, Nextflow work directories, Docker storage, and temporary files should remain outside GitHub. Keep only code, reusable configuration templates, concise reports, and small non-sensitive QC summaries in version control. Do not commit credentials or machine-specific paths.

## Interpretation

These are workflow-level validation results, not clinical conclusions. A count of VCF records is not equivalent to a count of clinically significant mutations. Any biological interpretation requires review of filtering, annotation, sample provenance, and relevant quality metrics.
