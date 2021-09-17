#!/usr/bin/env Rscript
library(htmlwidgets)
library(tidyverse)
library(plotly)

args <- commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("Missing table containing the benchmark results.", call.=FALSE)
} else if (length(args)==1) {
  fdr_csv <- args[1]
}

fdr <- read_csv(fdr_csv)

p_fdr_control <- fdr %>%
    mutate(fdr = ifelse(fdr == -1, 0, fdr),
           n = paste0('n = ', n),
           p = paste0('p = ', p)) %>%
    group_by(AM, n, p, alpha) %>%
    summarize(se = 1.96 * sd(fdr) / sqrt(n()),
              fdr = mean(fdr)) %>%
    mutate(nxp = paste(n, p)) %>%
    ggplot(aes(alpha, fdr, color = AM)) +
        geom_abline(slope = 1) +
        geom_errorbar(aes(ymin = fdr - se, ymax = fdr + se), width = .02) +
        geom_point() +
        geom_line() +
        facet_wrap(. ~ nxp) +
        labs(color = 'Algorithm', y = 'FDR') +
        theme(legend.position = 'bottom',
              text = element_text(size = 25))

saveWidget(ggplotly(p_fdr_control), file = "fdr_control.html")

p_empty_sets <- fdr %>%
    group_by(AM, alpha) %>%
    summarize(n = n(),
              no_solution = sum(fdr == -1)) %>%
    ggplot(aes(x = alpha, y = no_solution, fill = AM)) +
        geom_bar(stat = 'identity', position = 'dodge') +
        labs(fill = 'Algorithm', y = '# no solutions') +
        theme(legend.position = 'bottom',
              text = element_text(size = 25))

saveWidget(ggplotly(p_empty_sets), file = "empty_set.html")

