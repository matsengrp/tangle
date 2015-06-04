#!/usr/bin/Rscript --vanilla

library(ape)
library(dendextend)

args <- commandArgs(TRUE)

if(!(length(args) %in% c(3, 4))) {
    cat("Usage: idx_file which_tangle_one_idx out_file\n")
    stop()
}

idx_file <- args[1]
which_tangle <- args[2]
out_file <- args[3]

plot_fun <- ifelse(
        length(args) == 4,
        function(x) plot(x, use.edge.length = FALSE, main = args[4], axes=FALSE, leaflab="none"),
        function(x) plot(x, use.edge.length = FALSE, axes=FALSE, leaflab="none"))


df <- read.table(idx_file, stringsAsFactors=FALSE)
w = as.integer(which_tangle)
if(w > nrow(df)) {
  print("One-indexed tangle number argument too large.")
  stop()
}
t1 <- df[w, 3]
t2 <- df[w, 4]

dendrogram_of_newick <- function(s) {
  if(is.na(s) || !grep(';',s)) {
    cat("Bad looking tree: ")
    print(s)
    stop()
  }
  t <- read.tree(text=s)
  if(!(is.rooted(t)))
    t <- root(t, 1, resolve.root=TRUE)
  t$edge.length <- 1
  as.dendrogram(as.hclust(chronos(t)))
}


dl <- dendlist(dendrogram_of_newick(t1),dendrogram_of_newick(t2))
svg(out_file)
dl %>%
    untangle(method = "step2side") %>%
    set("branches_lwd", 3) %>%  # Thicken branches.
    plot_fun
dev.off()
