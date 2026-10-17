# Workflow

1. Retrieve NCBI SRA RunInfo for PRJNA637763.
2. Identify IBS and healthy-control samples from public sample metadata.
3. Resolve runs to ENA FASTQ files.
4. Import forward reads into QIIME 2.
5. Denoise with Deblur at 120 nt.
6. Classify ASVs with SILVA 138 99%.
7. Calculate alpha diversity and genus-level abundance.
8. Filter genera by prevalence and apply CLR transformation.
9. Evaluate L1 logistic regression and random forest using five-fold stratified cross-validation.
10. Commit compact tables, figures, metrics and provenance only.

The public SRA record identifies V1–V2 amplicons. Primer sequences are not assumed when they are not supported by the public record used for this workflow.
