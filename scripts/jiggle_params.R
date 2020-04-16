library(readr)
library(ggpubr)

### Load Data ###
raxml_iqtree_ll_all <- read_csv(
  "src/covid-19/results-full-ds/raxml_iqtree_ll_all.csv",
  skip = 3,
  col_types = cols(
    raxmlng = col_double(),
    iqtree = col_double()
))

gamma_ll_all <- read_csv(
  "src/covid-19/results-full-ds/gamma_ll_all.csv",
  skip = 2,
  col_types = cols(
    raxmlng = col_double(),
    iqtree = col_double(),
    raxml = col_double()
))

gamma_median_ll_all <- read_csv(
  "src/covid-19/results-full-ds/gamma_median_ll_all.csv",
  skip = 2,
  col_types = cols(
    raxmlng = col_double(),
    iqtree = col_double()
  ))

### Visualize ###

## GTR+FO+R4 ##
ggscatter(
    raxml_iqtree_ll_all,
    x = "raxmlng", y = "iqtree", 
    add = "reg.line", conf.int = TRUE, 
    cor.coef = TRUE, cor.method = "spearman",
    xlab = "RAxML-ng LNL", ylab = "iqtree LNL"
  ) +
  scale_x_reverse() + 
  scale_y_reverse()

## GTR+FO+G ##
ggscatter(
  gamma_ll_all,
  x = "raxmlng", y = "iqtree", 
  add = "reg.line", conf.int = TRUE, 
  cor.coef = TRUE, cor.method = "spearman",
  xlab = "RAxML-ng LNL", ylab = "iqtree LNL"
) +
  scale_x_reverse() + 
  scale_y_reverse()

ggscatter(
  gamma_ll_all,
  x = "raxmlng", y = "raxml", 
  add = "reg.line", conf.int = TRUE, 
  cor.coef = TRUE, cor.method = "spearman",
  xlab = "RAxML-ng LNL", ylab = "iqtree LNL"
) +
  scale_x_reverse() + 
  scale_y_reverse()

ggscatter(
  gamma_median_ll_all,
  x = "raxmlng", y = "iqtree", 
  add = "reg.line", conf.int = TRUE, 
  cor.coef = TRUE, cor.method = "spearman",
  xlab = "RAxML-ng LNL", ylab = "iqtree LNL"
) +
  scale_x_reverse() + 
  scale_y_reverse()

#### Hard facts ###

## GTR+FO+G ##

# Maximum absolute/relative difference  and correlation between RAxML-ng and iqtree
max((gamma_ll_all$raxmlng - gamma_ll_all$iqtree))
max((gamma_ll_all$raxmlng - gamma_ll_all$iqtree) / min(gamma_ll_all$raxmlng, gamma_ll_all$iqtree))

cor(gamma_ll_all$raxmlng, gamma_ll_all$iqtree, method = "spearman")
