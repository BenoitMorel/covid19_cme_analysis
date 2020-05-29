#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import pargenes_launcher
import mptp_launcher
from collections import Counter
from statistics import pvariance

paths = common.Paths( sys.argv )

def get_species_count(path : str) -> int:
  lines = open(path)
  for line in lines:
    if line.startswith("Number of delimited species"):
      return int(line.split(": ")[1])
  return -1

def summarize_species(n_trees: int, spec_counts: dict, csv_outpath: str, summary_outpath: str) -> None:
  ml_counts = [x[0] for x in spec_counts]
  mcmc_counts = [x[1] for x in spec_counts]
  csv_file = open(csv_outpath, 'w')
  csv_file.write('tree_idx, species_count_ml, species_count_mcmc')
  for i in range(n_trees):
    csv_file.write(str(i) + ',' + str(spec_counts[i][0]) + ',' + str(spec_counts[i][1]))
  csv_file.close()
  ml_hist = Counter(ml_counts)
  mcmc_hist = Counter(mcmc_counts)
  summary_file = open(summary_outpath, 'w')

  summary_file.write('Species count histogram for ml:')
  min_ml_count = min(ml_counts)
  max_ml_count = max(ml_counts)
  summary_file.write('Minimum species count for ml: ' + str(min_ml_count))
  summary_file.write('Maximum species count for ml: ' + str(max_ml_count))
  summary_file.write('Average species count for ml: ' + str(sum(ml_counts) / len(ml_counts)))
  summary_file.write('Species count variance for ml: ' + str(pvariance(ml_counts)))
  summary_file.write('\nSpecies count histogram for ml:')
  for x in ml_hist:
    if ml_hist[x] > 0:
      summary_file.write(str(x) + ': ' + str(ml_hist[x]))

  summary_file.write('Species count histogram for mcmc:')
  min_mcmc_count = min(mcmc_counts)
  max_mcmc_count = max(mcmc_counts)
  summary_file.write('Minimum species count for mcmc: ' + str(min_mcmc_count))
  summary_file.write('Maximum species count for mcmc: ' + str(max_mcmc_count))
  summary_file.write('Average species count for mcmc: ' + str(sum(mcmc_counts) / len(mcmc_counts)))
  summary_file.write('Species count variance for mcmc: ' + str(pvariance(mcmc_counts)))
  summary_file.write('\nSpecies count histogram for mcmc:')
  for x in mcmc_hist:
    if mcmc_hist[x] > 0:
      summary_file.write(str(x) + ': ' + str(mcmc_hist[x]))
  summary_file.close()

# run mptp on a NEWICK file with multiple rooted trees, separated line by line
# create a csv file with tree_id, species_count_ml, species_count_mcmc in it
# also create a summary text file with a species count histogram, min species count, max species count, and species count standard deviation
def run_mptp_on_trees(treesfile: str, output_path: str, csv_outpath: str, summary_outpath: str, mptp_fix: bool) -> None:
  lines = open(treesfile).lines()
  spec_counts = {}
  for i in range(len(lines)):
    tmp_tree_path = "tmp_tree.newick"
    outfile = open(tmp_tree_path, 'w')
    outfile.write(lines[i])
    outfile.close()
    results_mcmc = output_path_mcmc + "/" + str(i) + "/mcmc_output"
    results_ml = optput_path_ml + "/" + str(i) + "/ml_output"
    if not mptp_fix:
      mptp_launcher.launch_mptp(tmp_tree_path, results_ml)
      mptp_launcher.launch_mptp_mcmc(tmp_tree_path, results_mcmc)
    else:
      mptp_launcher.launch_mptp_fixed(tmp_tree_path, results_ml)
      mptp_launcher.launch_mptp_mcmc_fixed(tmp_tree_path, results_mcmc)
    species_ml = get_species_count(results_ml + ".txt")
    species_mcmc = get_species_count(results_mcmc + ".txt")
    species_counts[i] = (species_ml, species_mcmc)
    os.remove(tmp_tree_path)
  summarize_species(len(lines), spec_counts, csv_outpath, summary_outpath)
