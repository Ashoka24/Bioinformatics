# 03 — Public Shotgun Metagenomics Taxonomic Profiling

End-to-end shotgun metagenomics workflow using a real public human infant fecal WGS sample.

## Dataset

- BioProject: PRJNA273761
- Study: Metagenomes from human infant fecal samples with and without necrotizing enterocolitis
- Run analyzed: SRR1779146
- BioSample: SAMN03295851
- Experiment: SRX858749
- Study accession: SRP052967
- Instrument: Illumina HiSeq 2000
- Library strategy: WGS
- Layout: paired-end
- Analysis scope: one public paired-end WGS run, selected for reproducible GitHub-hosted execution

## Workflow

~~~text
NCBI/ENA public WGS run
        ↓
Paired FASTQ
        ↓
FASTP QC + adapter detection
        ↓
Kraken2 taxonomic classification
        ↓
Centrifuge taxonomic classification
        ↓
Independent classifier comparison
        ↓
Top-taxa + QC + provenance reports
~~~

Kraken2 and Centrifuge are run independently on the same cleaned paired-end reads. This makes the comparison methodological rather than treating one classifier as ground truth.

## Reference databases

### Kraken2

A maintained **Standard-8 Kraken2/Bracken index, June 2026**, from the Langmead Lab AWS Open Data index zone. The archive is 5.5 GB and the resulting database is capped at 8 GB. The index contains RefSeq archaea, bacteria, viral, plasmid, human and UniVec Core sequences. Reduced indexes trade some sensitivity/accuracy for smaller size.

### Centrifuge

The workflow uses the compressed bacteria + human + viral Centrifuge index hosted by the Langmead Lab AWS index infrastructure.

## Reproducibility

The workflow:

1. Downloads the pinned public FASTQ pair for SRR1779146 from ENA.
2. Runs FASTP and records the JSON QC summary.
3. Downloads the pinned June 2026 Kraken2 Standard-8 database over HTTPS.
4. Runs Kraken2 on the cleaned paired-end reads.
5. Removes the large Kraken2 database before downloading the Centrifuge index.
6. Runs Centrifuge on the same cleaned reads.
7. Generates top-taxa and classifier-comparison tables.
8. Commits only compact derived results; raw FASTQ, databases and per-read Centrifuge classifications are not committed.

## Results

The workflow creates:

- REPORT.md
- run_metadata.tsv
- fastp_summary.json
- kraken2.report
- top_taxa.tsv
- centrifuge.report.tsv
- classifier_comparison.tsv
- CLASSIFIER_COMPARISON.md

**Verified GitHub Actions run #15:** both classifiers completed and derived files were committed. Kraken2 classified **6,940,503 / 7,954,717 fragments (87.25%)**. The leading Kraken2 species was **Enterobacter roggenkampii (17.06% of total fragments)**. The top-10 classifier species overlap was **7/10 (Jaccard 0.5385)**. See results/REPORT.md and results/CLASSIFIER_COMPARISON.md.

## Interpretation boundary

This is a **single-run taxonomic profile**. It cannot establish NEC-associated taxa, biomarkers, causality, prevalence, or cohort-level differences. A biological comparison would require the full study cohort, consistent metadata, appropriate compositional/statistical analysis and multiple-testing control.

## Local execution

~~~bash
bash scripts/run_shotgun.sh
~~~

## Repository structure

~~~text
03_shotgun_metagenomics/
├── README.md
├── metadata/DATASET.md
├── scripts/
│   ├── run_shotgun.sh
│   ├── summarize_kraken.py
│   └── compare_classifiers.py
└── results/
~~~
