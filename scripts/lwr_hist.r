#!/usr/bin/env Rscript

library(ggplot2)
library(readr)
library(tidyr)
library(dplyr)
library(stringr)

args = commandArgs(trailingOnly=TRUE)

in_csv="lwr_histogram.csv"
out_plot="lwr_histogram.pdf"

if (length(args) >= 1) {
  in_csv=args[1]
}
if (length(args) == 2) {
  out_plot=args[2]
}

if (!file.exists(in_csv)) {
  print("No such file: ", in_csv)
  exit(1)
}

lwr_data <- read.csv(in_csv, header = TRUE)

lwr_data %>%
  select(Range, starts_with("Percentage.")) %>%
  rename_at(vars(starts_with("Percentage.")), 
    funs(str_replace(., "Percentage.", "Hit #"))) %>%
  gather("Type", "Value",-Range) %>%
  ggplot(aes(Range, Value, fill = Type)) +
  geom_bar(position = "dodge", stat = "identity") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust=1)) +
  xlab("LWR Range") +
  ylab("% of placements")

ggsave(out_plot)
