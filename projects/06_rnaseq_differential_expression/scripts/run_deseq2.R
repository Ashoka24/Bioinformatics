#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(DESeq2)
  library(ggplot2)
})

dir.create("results/figures", showWarnings = FALSE, recursive = TRUE)

count_url <- "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE116139&file=GSE116139_BulkRNAseqCounts.txt.gz&format=file"
input <- file.path(tempdir(), "GSE116139_BulkRNAseqCounts.txt.gz")
download.file(count_url, input, mode = "wb", quiet = TRUE)

meta <- data.frame(
  sample = c(
    "GSM3211196","GSM3211194","GSM3211169","GSM3211171",
    "GSM3211174","GSM3211175","GSM3211177","GSM3211178",
    "GSM3211186","GSM3211185","GSM3211180","GSM3211179",
    "GSM3211183","GSM3211182","GSM3211189","GSM3211190",
    "GSM3211193","GSM3211191"
  ),
  subject = factor(c(19,19,34,34,40,40,42,42,43,43,47,47,49,49,53,53,56,56)),
  tissue = factor(
    c("mucosa","blood","mucosa","blood","mucosa","blood","mucosa","blood",
      "mucosa","blood","mucosa","blood","mucosa","blood","mucosa","blood",
      "mucosa","blood"),
    levels = c("blood","mucosa")
  ),
  sample_title = c(
    "Subject19_mucosa_CD69-","Subject19_blood_CD69-",
    "Subject34_mucosa_CD69-","Subject34_blood_CD69-",
    "Subject40_mucosa_CD69-","Subject40_blood_CD69-",
    "Subject42_mucosa_CD69-","Subject42_blood_CD69-",
    "Subject43_mucosa_CD69-","Subject43_blood_CD69-",
    "Subject47_mucosa_CD69-","Subject47_blood_CD69-",
    "Subject49_mucosa_CD69-","Subject49_blood_CD69-",
    "Subject53_mucosa_CD69-","Subject53_blood_CD69-",
    "Subject56_mucosa_CD69-","Subject56_blood_CD69-"
  )
)
rownames(meta) <- meta$sample

raw <- read.delim(gzfile(input), check.names = FALSE, comment.char = "", stringsAsFactors = FALSE)
raw_names <- colnames(raw)

# NCBI's count matrix exposes 28 internal library IDs. The GEO series
# contains the same 28 samples in series order; validate the one-to-one map.
gsm <- c(
  "GSM3211169","GSM3211170","GSM3211171","GSM3211172","GSM3211173","GSM3211174",
  "GSM3211175","GSM3211176","GSM3211177","GSM3211178","GSM3211179","GSM3211180",
  "GSM3211181","GSM3211182","GSM3211183","GSM3211184","GSM3211185","GSM3211186",
  "GSM3211187","GSM3211188","GSM3211189","GSM3211190","GSM3211191","GSM3211192",
  "GSM3211193","GSM3211194","GSM3211195","GSM3211196"
)
libraries <- c(
  "lib10819","lib10820","lib10821","lib10823","lib11819","lib11820","lib11821",
  "lib11822","lib11823","lib11824","lib12778","lib12779","lib12780","lib12783",
  "lib12784","lib12785","lib12786","lib12787","lib12788","lib12791","lib12792",
  "lib12793","lib12794","lib12795","lib12796","lib7438","lib7439","lib7440"
)

if (length(gsm) != 28 || length(libraries) != 28) {
  stop("Expected 28 GEO samples and 28 count-matrix library columns")
}
if (!all(libraries %in% raw_names)) {
  stop("Validated library mapping contains IDs absent from the count matrix")
}

mapping <- data.frame(gsm = gsm, library_name = libraries, stringsAsFactors = FALSE)
write.table(mapping, "results/library_mapping.tsv", sep = "\t", quote = FALSE, row.names = FALSE)

sample_idx <- match(meta$sample, mapping$gsm)
meta$library_id <- mapping$library_name[sample_idx]

gene_candidates <- c("gene_id", "Geneid", "gene", "Gene")
gene_col <- gene_candidates[gene_candidates %in% raw_names][1]
if (is.na(gene_col)) gene_col <- raw_names[1]

library_idx <- match(meta$library_id, raw_names)
if (anyNA(library_idx)) stop("One or more mapped libraries are absent from the count matrix")
counts <- raw[, c(1, library_idx), drop = FALSE]
colnames(counts)[1] <- "gene_id"
colnames(counts)[-1] <- meta$sample
counts$gene_id <- as.character(counts$gene_id)
counts <- counts[counts$gene_id != "" & !duplicated(counts$gene_id), , drop = FALSE]
rownames(counts) <- counts$gene_id
counts$gene_id <- NULL

counts[] <- lapply(counts, function(x) as.numeric(as.character(x)))
counts[is.na(counts)] <- 0
counts <- round(as.matrix(counts))

meta <- meta[colnames(counts), , drop = FALSE]
stopifnot(all(rownames(meta) == colnames(counts)))

keep <- rowSums(counts >= 10) >= 9
counts <- counts[keep, , drop = FALSE]

dds <- DESeqDataSetFromMatrix(countData = counts, colData = meta, design = ~ subject + tissue)
dds <- DESeq(dds)

res <- as.data.frame(results(dds, contrast = c("tissue", "mucosa", "blood")))
res$gene_id <- rownames(res)
res <- res[order(res$padj, -abs(res$log2FoldChange)), ]
write.table(res, "results/differential_expression.tsv", sep = "\t", quote = FALSE, row.names = FALSE)

norm <- counts(dds, normalized = TRUE)
norm_out <- data.frame(gene_id = rownames(norm), norm, check.names = FALSE)
write.table(norm_out, "results/normalized_counts.tsv", sep = "\t", quote = FALSE, row.names = FALSE)

sig <- subset(res, !is.na(padj) & padj < 0.05 & abs(log2FoldChange) >= 1)

vsd <- vst(dds, blind = FALSE)
pca <- plotPCA(vsd, intgroup = c("tissue", "subject"))
ggsave("results/figures/01_pca.svg", pca, width = 7, height = 5)

res_plot <- res[!is.na(res$padj), ]
res_plot$significant <- ifelse(res_plot$padj < 0.05 & abs(res_plot$log2FoldChange) >= 1,
                               "Significant", "Not significant")
p <- ggplot(res_plot, aes(x = log2FoldChange, y = -log10(padj), color = significant)) +
  geom_point(alpha = 0.5, size = 1) +
  theme_minimal() +
  labs(title = "Mucosa vs blood: differential expression",
       x = "log2 fold change", y = "-log10 adjusted p-value") +
  theme(legend.title = element_blank())
ggsave("results/figures/02_volcano_plot.svg", p, width = 7, height = 5)

report <- c(
  "# Verified Run", "",
  paste0("- Input samples: ", nrow(meta)),
  paste0("- Subjects: ", length(unique(meta$subject))),
  paste0("- Genes after low-count filtering: ", nrow(counts)),
  paste0("- Significant genes (padj < 0.05, |log2FC| >= 1): ", nrow(sig)),
  "", "## Top genes", "",
  capture.output(print(head(res[, c("gene_id","log2FoldChange","pvalue","padj")], 15),
                        row.names = FALSE))
)
writeLines(report, "results/REPORT.md")
