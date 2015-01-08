#!/usr/bin/Rscript --vanilla

library(ape)
library(dendextend)

args <- commandArgs(TRUE)

stopifnot(length(args) == 3)

idx_file <- args[1]
which_tangle <- args[2]
out_file <- args[3]

df <- read.table(idx_file, stringsAsFactors=FALSE)
t1 <- df[which_tangle, 3]
t2 <- df[which_tangle, 4]

dendrogram_of_newick <- function(s) {
  t <- read.tree(text=s)
  t$edge.length <- 1
  as.dendrogram(as.hclust(chronos(t)))
}


dl <- dendlist(dendrogram_of_newick(t1),dendrogram_of_newick(t2))
svg(out_file)
dl %>%
    untangle(method = "step2side") %>%
    plot(use.edge.length = FALSE)
dev.off()
