# Outcomes and Deliverables — Project 01

This project separates **expected workflow outputs** from **measured biological results**. No numerical result is reported here until the public dataset has actually been processed.

## 1. Outcome chain

| Stage | Expected outcome | Primary files |
|---|---|---|
| NCBI download | Valid public SRA record converted to paired FASTQ | `*.sra`, `*_1.fastq.gz`, `*_2.fastq.gz` |
| Integrity check | Download verified and paired reads confirmed | `sha256sums.txt` |
| Read QC | Per-read quality and adapter/sequence-content assessment | FastQC `.html`, `.zip`; MultiQC `.html` |
| Input preparation | Analysis-ready paired FASTQ references | `input/` symlinks |
| Amplicon processing | Denoised features/ASVs and taxonomy | QIIME 2 `.qza` artifacts |
| Diversity analysis | Descriptive alpha/beta diversity outputs | tables, visualizations, QIIME 2 artifacts |
| Metadata expansion | Parent BioProject run metadata | `PRJNA1031545_runinfo.csv` |
| Interpretation | Evidence-based technical and biological observations | documented report/figures |

## 2. Figures to produce after execution

The repository should eventually contain figures generated from the **actual public dataset**, not illustrative numbers.

### Figure 1 — Read quality

Show the FastQC/MultiQC quality profile for R1 and R2.

Questions:

- Is per-base sequence quality acceptable?
- Where does quality decline?
- Are adapter/primer signals present?
- Are the paired reads suitable for the selected truncation lengths?

Source:
`QC/multiqc/multiqc_report.html`

### Figure 2 — Feature/taxon composition

After successful amplicon processing, show the most abundant taxa at a clearly stated taxonomic level.

Do not assign biological meaning before checking:

- taxonomy confidence;
- feature prevalence;
- sequencing depth;
- sample count.

### Figure 3 — Alpha diversity

For a single run, report descriptive metrics only, such as:

- observed features;
- Shannon diversity.

Do not present a single-sample value as a group comparison.

### Figure 4 — Beta diversity / ordination

For the eventual multi-sample BioProject analysis, generate an appropriate beta-diversity distance matrix and ordination such as PCoA.

A one-sample dataset cannot provide a meaningful between-sample ordination.

### Figure 5 — Cohort-level taxonomic comparison

Only after the parent BioProject metadata have been inspected and valid biological groups have been defined.

Potential outputs include:

- taxonomic abundance comparison;
- differential abundance;
- effect sizes;
- statistical significance;
- multiple-testing correction.

## 3. Current status

**Workflow status:** repository and execution framework prepared.

**Biological-results status:** pending actual execution on the public NCBI data.

This distinction is intentional. The portfolio must not contain fabricated abundance tables, diversity values, p-values, or biological conclusions.

## 4. File layout after execution

```text
16s_ncbi_gut/
├── RawData/
│   └── SRR26534086/
│       ├── sra/
│       ├── fastq/
│       ├── checksums/
│       └── input/
├── QC/
│   ├── fastqc/
│   └── multiqc/
├── Analysis/
│   └── ampliseq/
├── Logs/
└── metadata/
```

The generated data remain outside Git. The repository stores the scripts, parameters, metadata definitions, documentation and final figures/results only when they have actually been generated.

## 5. Portfolio-facing outcome

The final project should demonstrate:

**public biological data → reproducible download → integrity validation → QC → amplicon processing → taxonomy → diversity analysis → biological interpretation → documented limitations**

That is the primary portfolio outcome, rather than a fabricated biological claim from one sample.
