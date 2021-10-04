#!/usr/bin/env Rscript

library(SummarizedExperiment)
library(TCGAbiolinks)
library(tidyverse)
library(reticulate)

query <- GDCquery(project = "TCGA-BRCA",
                  data.category = "Transcriptome Profiling",
                  data.type = "Gene Expression Quantification",
                  workflow.type = "HTSeq - FPKM-UQ")
GDCdownload(query)
data <- GDCprepare(query)

# select samples from tumor and normal tissue
sample_info <- as_tibble(colData(data))

sample_type <- colData(data)$sample_type
accepted_sample_types <- c("Primary Tumor", "Solid Tissue Normal")
samples_keep <- sample_type %in% accepted_sample_types

# save data as numpy object
X <- t(assay(data)[,samples_keep])
y <- as.integer(sample_type[samples_keep] == "Primary Tumor") * 2 - 1
genes <- rowData(data)$external_gene_name

# balance samples
samples_per_class <- min(table(y))

X0 <- X[y == -1,][1:samples_per_class,]
X1 <- X[y == 1,][1:samples_per_class,]
X <- rbind(X0, X1)

y <- c(rep(-1, samples_per_class), rep(1, samples_per_class))

np <- import("numpy")
np$savez("Xy.npz", X=X, Y=y, genes=genes)
