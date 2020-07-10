#!/usr/bin/env python3

import os
import sys
import shutil
sys.path.insert(0, 'scripts')
import common
import mptp_launcher
from collections import Counter
from statistics import pvariance
import glob
import util

def get_species_count(path : str) -> int:
  lines = open(path)
  for line in lines:
    if line.startswith("Number of delimited species"):
      return int(line.split(": ")[1])
  return -1

def summarize_species(n_trees: int, spec_counts: dict, csv_outpath: str, summary_outpath: str) -> None:
  ml_counts = [spec_counts[i][0] for i in range(n_trees)]
  mcmc_counts = [spec_counts[i][1] for i in range(n_trees)]
  csv_file = open(csv_outpath, 'w')
  csv_file.write('tree_idx, species_count_ml, species_count_mcmc\n')
  for i in range(n_trees):
    csv_file.write(str(i) + ',' + str(spec_counts[i][0]) + ',' + str(spec_counts[i][1]) + '\n')
  csv_file.close()
  ml_hist = Counter(ml_counts)
  mcmc_hist = Counter(mcmc_counts)
  summary_file = open(summary_outpath, 'w')

  min_ml_count = min(ml_counts)
  max_ml_count = max(ml_counts)
  summary_file.write('Minimum species count for ml: ' + str(min_ml_count) + '\n')
  summary_file.write('Maximum species count for ml: ' + str(max_ml_count) + '\n')
  summary_file.write('Average species count for ml: ' + str(sum(ml_counts) / len(ml_counts)) + '\n')
  summary_file.write('Species count variance for ml: ' + str(pvariance(ml_counts)) + '\n')
  summary_file.write('\nSpecies count histogram for ml:\n')
  for x in ml_hist:
    if ml_hist[x] > 0:
      summary_file.write(str(x) + ': ' + str(ml_hist[x]) + '\n')

  summary_file.write('\n\n')
  min_mcmc_count = min(mcmc_counts)
  max_mcmc_count = max(mcmc_counts)
  summary_file.write('Minimum species count for mcmc: ' + str(min_mcmc_count) + '\n')
  summary_file.write('Maximum species count for mcmc: ' + str(max_mcmc_count) + '\n')
  summary_file.write('Average species count for mcmc: ' + str(sum(mcmc_counts) / len(mcmc_counts)) + '\n')
  summary_file.write('Species count variance for mcmc: ' + str(pvariance(mcmc_counts)) + '\n')
  summary_file.write('\nSpecies count histogram for mcmc:\n')
  for x in mcmc_hist:
    if mcmc_hist[x] > 0:
      summary_file.write(str(x) + ': ' + str(mcmc_hist[x]) + '\n')
  summary_file.close()

# run mptp on a NEWICK file with multiple rooted trees, separated line by line
# create a csv file with tree_id, species_count_ml, species_count_mcmc in it
# also create a summary text file with a species count histogram, min species count, max species count, and species count variance
def run_mptp_on_trees(treesfile: str, output_path: str, csv_outpath: str, summary_outpath: str, mptp_fix: bool) -> None:
  lines = open(treesfile).readlines()
  spec_counts = {}
  util.mkdirp(output_path)
  for i in range(len(lines)):
    tmp_tree_path = os.path.join(output_path, "tmp_tree.newick")
    outfile = open(tmp_tree_path, 'w')
    outfile.write(lines[i])
    outfile.close()
    results_mcmc = output_path + "/" + str(i) + "/mcmc_output"
    results_ml = output_path + "/" + str(i) + "/ml_output"
    if os.path.isdir(results_mcmc):
      shutil.rmtree(results_mcmc)
    if os.path.isdir(results_ml):
      shutil.rmtree(results_ml)
    os.makedirs(results_mcmc)
    os.makedirs(results_ml)
    if not mptp_fix:
      mptp_launcher.launch_mptp(tmp_tree_path, results_ml + "/output")
      mptp_launcher.launch_mptp_mcmc(tmp_tree_path, results_mcmc + "/output")
    else:
      mptp_launcher.launch_mptp_fixed(tmp_tree_path, results_ml + "/output")
      mptp_launcher.launch_mptp_mcmc_fixed(tmp_tree_path, results_mcmc + "/output")
    species_ml = get_species_count(results_ml + "/output.txt")
    mcmc_outfile_path = glob.glob(os.path.join(results_mcmc, 'output.*.txt'))[0]
    species_mcmc = get_species_count(mcmc_outfile_path)
    spec_counts[i] = (species_ml, species_mcmc)
    os.remove(tmp_tree_path)
  summarize_species(len(lines), spec_counts, csv_outpath, summary_outpath)

if __name__ == "__main__":
  paths = common.Paths( sys.argv )
  run_mptp_on_trees(paths.raxml_credible_ml_trees, paths.mptp_output, paths.mptp_output_csv, paths.mptp_output_summary, mptp_fix = False)

  # TODO: add usage of genesis_mptp_all_rootings in order to create summary statistics regarding all possible rootings
