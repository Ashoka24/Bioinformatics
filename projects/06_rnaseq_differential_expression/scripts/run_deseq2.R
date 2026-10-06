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
  )
)
rownames(meta) <- meta$sample

raw <- read.delim(gzfile(input), check.names = FALSE, comment.char = "", stringsAsFactors = FALSE)
raw_names <- colnames(raw)

# NCBI's matrix uses internal library IDs. Resolve them through ENA metadata,
# retaining the GEO GSM accession via secondary_sample_accession.
ena_url <- paste0(
  "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run",
  "&query=secondary_study_accession%3D%22SRP151065%22",
  "&fields=sample_accession,secondary_sample_accession,library_name",
  "&format=tsv&limit=1000"
)
ena_file <- file.path(tempdir(), "GSE116139_ena.tsv")
download.file(ena_url, ena_file, mode = "wb", quiet = TRUE)
ena <- read.delim(ena_file, check.names = FALSE, stringsAsFactors = FALSE)

required <- c("sample_accession", "secondary_sample_accession", "library_name")
if (!all(required %in% colnames(ena))) {
  stop(sprintf("ENA metadata missing required columns: %s",
              paste(setdiff(required, colnames(ena)), collapse = ", ")))
}

# Some records may have multiple runs. Keep the first library record for each GSM.
ena$secondary_sample_accession <- trimws(ena$secondary_sample_accession)
ena$library_name <- trimws(ena$library_name)
ena <- ena[ena$secondary_sample_accession %in% meta$sample, , drop = FALSE]
ena <- ena[!duplicated(ena$secondary_sample_accession), , drop = FALSE]

sample_idx <- match(meta$sample, ena$secondary_sample_accession)
if (anyNA(sample_idx)) {
  print(ena)
  stop(sprintf("Could not resolve GSM samples through ENA metadata: %s",
               paste(meta$sample[is.na(sample_idx)], collapse = ", ")))
}

meta$library_id <- ena$library_name[sample_idx]

missing_libs <- setdiff(meta$library_id, raw_names)
if (length(missing_libs) > 0) {
  stop(sprintf("ENA-resolved library IDs absent from count matrix: %s",
               paste(missing_libs, collapse = ", ")))
}

gene_candidates <- c("gene_id", "Geneid", "gene", "Gene")
gene_col <- gene_candidates[gene_candidates %in% raw_names][1]
if (is.na(gene_col)) gene_col <- raw_names[1]

counts <- raw[, c(gene_col, meta$library_id), drop = FALSE]
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
