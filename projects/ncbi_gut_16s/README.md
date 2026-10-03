# NCBI Human Gut 16S rRNA — End-to-End Analysis

This project is an end-to-end, reproducible 16S rRNA analysis using **openly available NCBI SRA human stool data**.

The workflow deliberately follows the operational workflow used in the supplied IOM 16S document, then extends it into a research-grade public-data workflow.

## Biological dataset

**Selected public SRA run:** `SRR26534086`

- Study: *Gut butyrate-producers confer post-infarction cardiac protection*
- BioProject: `PRJNA1031545`
- Sample: `SAMN37943185`
- Library: `HS100`
- Platform: Illumina MiSeq
- Layout: paired-end
- Assay: 16S amplicon
- Region: V3–V4
- Primers reported by NCBI: 319F/806R, with forward sequence `CCTACGGGNGGCWGCAG` and reverse sequence `GACTACHVGGGTATCTAATCC`
- Run size reported by NCBI: 49,964 spots / 22.5M bases / ~13.1 MB

NCBI describes this run as human gut metagenome/stool 16S data. citeturn3search1

### Why this sample?

It is useful for this portfolio because the public record provides:

1. human stool material;
2. paired-end Illumina data;
3. V3–V4 16S amplicon sequencing;
4. primer information compatible with the supplied IOM workflow;
5. a public SRA accession that can be downloaded reproducibly.

**Important:** one sample is sufficient to demonstrate the complete technical pipeline, but it is **not** sufficient for a group-level biological conclusion. The project therefore separates *pipeline validation* from *biological inference*.

For a real comparison, the same workflow can be expanded to multiple accessions from `PRJNA1031545`.

---

# 1. The workflow we are reproducing

The supplied IOM workflow starts with VM access and raw FASTQ collection, performs FastQC/MultiQC, prepares IDs, organizes storage, and runs nf-core/ampliseq with Docker. fileciteturn22file0L6-L30 fileciteturn22file0L38-L55 fileciteturn22file0L84-L102

I am keeping that workflow and adding the NCBI/public-data and downstream analysis layers:

```text
NCBI SRA
   │
   ▼
Prefetch / download
   │
   ▼
FASTQ extraction
   │
   ├── checksum / file validation
   │
   ▼
FastQC
   │
   ▼
MultiQC
   │
   ▼
Primer + read-length QC
   │
   ▼
Input organization
   │
   ▼
nf-core/ampliseq + Docker
   │
   ├── Cutadapt
   ├── DADA2
   ├── chimera removal
   ├── ASV inference
   ├── SILVA taxonomy
   └── QIIME 2 artifacts
   │
   ▼
QIIME 2 downstream
   │
   ├── feature table
   ├── taxonomy
   ├── alpha diversity
   ├── beta diversity
   ├── PCoA
   └── taxa relative abundance
   │
   ▼
Biological interpretation
   │
   ▼
Reproducible results + QC log
```

---

# 2. Directory layout on the VM

The paths are based on the storage convention in the supplied workflow. fileciteturn22file0L79-L87

I recommend creating a dedicated public-data project rather than mixing it with vendor data:

```text
/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis/
└── NCBI_Gut_16S/
    ├── RawData/
    │   └── SRR26534086/
    │       ├── sra/
    │       ├── fastq/
    │       └── checksums/
    ├── QC/
    │   ├── fastqc_raw/
    │   └── multiqc_raw/
    ├── Analysis/
    │   └── ampliseq/
    ├── Downstream/
    ├── Results/
    ├── Logs/
    ├── Metadata/
    ├── Params/
    └── work_dir/
```

Set the project path once:

```bash
export IOM16S="/home/azureuser/s3_bucket2/nftower/Iom_16s_analysis"
export PROJECT="$IOM16S/NCBI_Gut_16S"

mkdir -p "$PROJECT"/{RawData/SRR26534086/{sra,fastq,checksums},QC/{fastqc_raw,multiqc_raw},Analysis/ampliseq,Downstream,Results,Logs,Metadata,Params,work_dir}

echo "$PROJECT"
```

Do **not** hard-code private SSH keys or credentials into this repository.

---

# 3. Environment setup

The supplied workflow uses Docker with nf-core/ampliseq. fileciteturn22file0L88-L102

Check the VM:

```bash
uname -a
lsb_release -a || true
docker --version
docker info
nextflow -version
java -version
python3 --version
```

If Docker is installed but not running:

```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker
```

Test:

```bash
docker run --rm hello-world
```

For the SRA Toolkit:

```bash
sudo apt-get update
sudo apt-get install -y sra-toolkit pigz
```

Check:

```bash
prefetch --version
fasterq-dump --version
pigz --version
```

For QC:

```bash
sudo apt-get install -y fastqc
python3 -m pip install --user multiqc
```

Check:

```bash
fastqc --version
multiqc --version
```

---

# 4. NCBI data provenance

Create the accession manifest:

```bash
cat > "$PROJECT/Metadata/ncbi_accessions.tsv" <<'EOF'
sample_id	SRA_accession	biosample	bioproject	material	assay	region	layout
SRR26534086	SRR26534086	SAMN37943185	PRJNA1031545	human stool	16S amplicon	V3-V4	PAIRED
EOF
```

Create a provenance record:

```bash
cat > "$PROJECT/Metadata/data_provenance.txt" <<'EOF'
Source: NCBI Sequence Read Archive
SRA run: SRR26534086
BioSample: SAMN37943185
BioProject: PRJNA1031545
Data type: 16S rRNA amplicon
Material: human stool
Platform: Illumina MiSeq
Layout: paired-end
Forward primer: CCTACGGGNGGCWGCAG
Reverse primer: GACTACHVGGGTATCTAATCC
EOF
```

NCBI's public record reports the run as paired-end 16S amplicon sequencing of human stool and gives the primer sequences above. citeturn3search1

---

# 5. Download from NCBI SRA

## 5.1 Configure SRA cache

Use a storage location with sufficient free space:

```bash
mkdir -p "$PROJECT/RawData/SRR26534086/sra"

prefetch SRR26534086 \
    --output-directory "$PROJECT/RawData/SRR26534086/sra" \
    --max-size 10G
```

Check:

```bash
find "$PROJECT/RawData/SRR26534086/sra" -type f -ls
```

## 5.2 Extract paired FASTQ

```bash
mkdir -p "$PROJECT/RawData/SRR26534086/fastq"

fasterq-dump \
    "$PROJECT/RawData/SRR26534086/sra/SRR26534086/SRR26534086.sra" \
    --split-files \
    --threads 4 \
    --outdir "$PROJECT/RawData/SRR26534086/fastq"
```

Compress:

```bash
pigz -p 4 "$PROJECT/RawData/SRR26534086/fastq/"*.fastq
```

Expected paired files:

```text
SRR26534086_1.fastq.gz
SRR26534086_2.fastq.gz
```

Check:

```bash
ls -lh "$PROJECT/RawData/SRR26534086/fastq/"
```

---

# 6. Validate the downloaded FASTQ

Count reads:

```bash
for f in "$PROJECT"/RawData/SRR26534086/fastq/*.fastq.gz; do
    echo "FILE: $f"
    zcat "$f" | awk 'END {print "reads=" NR/4}'
done
```

Check paired read counts:

```bash
R1=$(zcat "$PROJECT/RawData/SRR26534086/fastq/SRR26534086_1.fastq.gz" | awk 'END{print NR/4}')
R2=$(zcat "$PROJECT/RawData/SRR26534086/fastq/SRR26534086_2.fastq.gz" | awk 'END{print NR/4}')

echo "R1=$R1"
echo "R2=$R2"

test "$R1" -eq "$R2" && echo "PAIR CHECK: PASS" || echo "PAIR CHECK: FAIL"
```

Generate checksums:

```bash
sha256sum "$PROJECT"/RawData/SRR26534086/fastq/*.fastq.gz \
    > "$PROJECT/RawData/SRR26534086/checksums/sha256sums.txt"
```

---

# 7. FastQC

This follows the QC stage in the supplied workflow. fileciteturn22file0L38-L55

```bash
mkdir -p "$PROJECT/QC/fastqc_raw"

fastqc \
    "$PROJECT"/RawData/SRR26534086/fastq/*.fastq.gz \
    --outdir "$PROJECT/QC/fastqc_raw" \
    --threads 4
```

The supplied document interprets FastQC broadly as green = acceptable, yellow = marginal and red = poor. fileciteturn22file0L57-L59

Do not blindly trim because a graph is yellow/red. Base the decision on per-base quality, adapter content, sequence length and the amplicon design.

---

# 8. MultiQC

```bash
mkdir -p "$PROJECT/QC/multiqc_raw"

multiqc "$PROJECT/QC/fastqc_raw" \
    --outdir "$PROJECT/QC/multiqc_raw" \
    --filename multiqc_raw.html
```

Record:

- total reads;
- read length;
- per-base quality;
- adapter content;
- sequence duplication;
- overrepresented sequences;
- N content.

---

# 9. Primer and read-length decision

The NCBI record reports V3–V4 16S and the same primer sequence context used in the supplied workflow. citeturn3search1

The supplied workflow specifies:

```text
FW_primer = CCTACGGGNGGCWGCAG
RV_primer = GACTACHVGGGTATCTAATCC

trunclenf = 280
trunclenr = 260

sample_inference = pseudo
qiime_ref_taxonomy = silva
skip_barrnap = true
skip_dada_taxonomy = true
skip_dada_addspecies = true
```

These values are retained as the baseline experiment because they are explicitly present in the supplied workflow. fileciteturn22file0L103-L123

**However:** truncation is data-dependent. Before a production run, inspect FastQC/MultiQC and verify that forward and reverse reads retain enough overlap for V3–V4 merging.

---

# 10. Prepare nf-core/ampliseq input

```bash
mkdir -p "$PROJECT/RawData/SRR26534086/input"

ln -sf \
    "$PROJECT/RawData/SRR26534086/fastq/SRR26534086_1.fastq.gz" \
    "$PROJECT/RawData/SRR26534086/input/SRR26534086_1.fastq.gz"

ln -sf \
    "$PROJECT/RawData/SRR26534086/fastq/SRR26534086_2.fastq.gz" \
    "$PROJECT/RawData/SRR26534086/input/SRR26534086_2.fastq.gz"

ls -lah "$PROJECT/RawData/SRR26534086/input/"
```

---

# 11. Run nf-core/ampliseq

The supplied workflow uses nf-core/ampliseq release 2.11.0 and Docker. fileciteturn22file0L88-L102

```bash
cd "$PROJECT"

nextflow run nf-core/ampliseq \
    -r 2.11.0 \
    -name NCBI_Gut_SRR26534086 \
    -work-dir "$PROJECT/work_dir/ampliseq" \
    -params-file "$PROJECT/Params/ampliseq_params.json" \
    -profile docker \
    -resume \
    2>&1 | tee "$PROJECT/Logs/ampliseq.log"
```

For a clean rerun, remove or change the work directory and omit `-resume`.

**Resource warning:** the supplied workflow specifies 3 CPUs and 12 GB, but DADA2 processes may require more RAM. If Nextflow reports `Process requirement exceeds available memory`, document the failure and increase VM resources or adjust the pipeline resource configuration.

---

# 12. What happens inside Ampliseq

```text
FASTQ
  │
  ├── primer removal / trimming
  ├── quality filtering
  ├── dereplication
  ├── DADA2 error-model learning
  ├── ASV inference
  ├── paired-end merging
  ├── chimera removal
  ├── SILVA taxonomy
  └── QIIME 2 artifacts
        │
        ├── feature table
        ├── representative sequences
        ├── taxonomy
        └── quality summaries
```

The important point is that the raw reads become a feature-by-sample matrix of ASVs, plus taxonomy and sequence artifacts.

---

# 13. Post-pipeline QC

Do not immediately make abundance plots.

Inspect:

```bash
find "$PROJECT/Analysis/ampliseq" -type f | sort | head -200

find "$PROJECT/Analysis/ampliseq" \
    \( -name "*.qza" -o -name "*.qzv" -o -name "*.tsv" \) \
    -print
```

Record:

- input reads;
- retained reads;
- ASV count;
- chimera removal;
- taxonomy assignment rate;
- unassigned fraction;
- sequencing depth.

---

# 14. QIIME 2 downstream

If QIIME 2 is installed:

```bash
conda activate qiime2
qiime --version
```

Export the feature table:

```bash
mkdir -p "$PROJECT/Downstream/feature_table"

qiime tools export \
    --input-path <feature_table.qza> \
    --output-path "$PROJECT/Downstream/feature_table"
```

Export taxonomy:

```bash
mkdir -p "$PROJECT/Downstream/taxonomy"

qiime tools export \
    --input-path <taxonomy.qza> \
    --output-path "$PROJECT/Downstream/taxonomy"
```

Replace the placeholders with the actual artifact paths generated by the run.

---

# 15. Relative abundance

For sample (j):

```text
relative abundance(i,j)
=
count(i,j) / total counts(j)
```

and:

```text
percentage = relative abundance × 100
```

Use this for descriptive abundance plots while remembering that microbiome abundance data are compositional.

---

# 16. Alpha diversity

Calculate:

- observed ASVs;
- Shannon diversity;
- optionally Simpson diversity.

Shannon:

```text
H' = -Σ pᵢ ln(pᵢ)
```

For the single technical-validation sample this is descriptive only. Statistical comparison requires multiple biological samples.

---

# 17. Beta diversity and PCoA

For multiple samples, calculate a distance matrix such as Bray–Curtis and perform PCoA.

With one sample, beta diversity and PCoA are not meaningful. This is intentional: the first run validates the complete technical path from NCBI to ASVs.

The next experiment should use multiple accessions from the same BioProject.

---

# 18. Biological interpretation

At genus level, generate:

1. top genera;
2. relative-abundance table;
3. abundance bar plot;
4. unclassified fraction;
5. sample-level QC summary.

For gut microbiome work, reasonable exploratory questions include:

- Which genera dominate?
- What fraction is assigned to known genera?
- How many ASVs remain after filtering?
- Which taxa are consistently detected across biological replicates?
- Does community structure differ between pre-defined groups?

Do not infer disease associations from this single sample.

---

# 19. Scale to a real biological experiment

After the single-run validation succeeds, expand the accession manifest to multiple runs from `PRJNA1031545`.

Use:

```text
sample_id    accession       biological_group
S01          SRRxxxxxxx      group_A
S02          SRRxxxxxxx      group_A
S03          SRRxxxxxxx      group_B
...
```

Then repeat:

```text
NCBI download
→ FASTQ validation
→ FastQC
→ MultiQC
→ Ampliseq
→ post-QC
→ taxonomy
→ alpha diversity
→ beta diversity
→ differential abundance
→ biological interpretation
```

Groups must come from study metadata, not be invented from the sequence data.

---

# 20. Reproducibility checklist

- [ ] NCBI accession recorded
- [ ] BioProject recorded
- [ ] BioSample recorded
- [ ] FASTQ checksum stored
- [ ] FastQC report stored
- [ ] MultiQC report stored
- [ ] primer sequences recorded
- [ ] truncation decision documented
- [ ] nf-core/ampliseq version recorded
- [ ] Nextflow version recorded
- [ ] Docker version recorded
- [ ] SILVA version recorded
- [ ] parameter JSON committed
- [ ] Nextflow log stored
- [ ] feature table exported
- [ ] taxonomy exported
- [ ] diversity results stored
- [ ] figures generated from code
- [ ] biological interpretation separated from technical QC
- [ ] limitations documented

---

# 21. What makes this look human/research-grade

The repository should show:

**Question → dataset → provenance → raw data → QC → parameter decision → pipeline → failure/retry when applicable → post-QC → statistics → visualization → biological interpretation → limitations.**

Do not hide failures. If DADA2 needs more RAM, record the actual error and the final resource decision in `Logs/RESOURCE_NOTES.md`.

That is much more credible than a repository containing only a final plot.

## Sources

- NCBI SRA: SRR26534086. citeturn3search1
- Supplied IOM 16S workflow. fileciteturn22file0L30-L55 fileciteturn22file0L84-L123
