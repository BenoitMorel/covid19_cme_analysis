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
from typing import List, Tuple

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

def get_all_rootings_counts(outfile: str) -> tuple:
  min_s, max_s, median_s = 0, 0, 0
  lines = open(outfile)
  for line in lines:
    if line.startswith("Minimum species count"):
      min_s = int(line.split(": ")[1])
    elif line.startswith("Maximum species count"):
      max_s = int(line.split(": ")[1])
    elif line.startswith("Median species count"):
      median_s = int(line.split(": ")[1])
  return (min_s, max_s, median_s)

def get_all_rootings_counts_one_histogram(outfile: str, species):
  lines = open(outfile)
  for i in range(4, len(lines)):
    species[int(line.split(",")[0])] += int(line.split(",")[1])
  return species

def summarize_species_all_rootings(n_trees: int, min_species: List[int], max_species: List[int], median_species: List[int], summary_outpath: str) -> None:
  min_hist = Counter(min_species)
  max_hist = Counter(max_species)
  median_hist = Counter(median_species)
  summary_file = open(summary_outpath, 'w')
  summary_file.write('The following 3 histograms show the distribution of min/max/median species count that was encountered when trying all rootings for a tree, and this taken over all trees in the input data set.\n\n')
  summary_file.write('Minimum species count histogram:\n')
  for x in min_hist:
    if min_hist[x] > 0:
      summary_file.write(str(x) + ': ' + str(min_hist[x]) + '\n')
  summary_file.write('\n\nMaximum species count histogram:\n')
  for x in max_hist:
    if max_hist[x] > 0:
      summary_file.write(str(x) + ': ' + str(max_hist[x]) + '\n')
  summary_file.write('\n\nMedian species count histogram:\n')
  for x in median_hist:
    if median_hist[x] > 0:
      summary_file.write(str(x) + ': ' + str(median_hist[x]) + '\n')
  summary_file.close()


def summarize_species_all_rootings_one_histogram(n_trees: int, species, summary_outpath: str) -> None:
  summary_file = open(summary_outpath, 'w')
  summary_file.write('The following histogram shows the distribution of species count that was encountered when trying all rootings for all trees in the input data set.\n\n')
  summary_file.write('Species count histogram:\n')
  for x in species:
    if species[x] > 0:
      summary_file.write(str(x) + ': ' + str(species[x]) + '\n')
  summary_file.close()

def run_mptp_all_rootings_on_trees(treesfile: str, output_path: str, summary_outpath: str) -> None:
  # This always uses vanilla mptp and never uses mptp_fix!
  lines = open(treesfile).readlines()
  min_species = []
  max_species = []
  median_species = []
  util.mkdirp(output_path)
  for i in range(len(lines)):
    tmp_tree_path = os.path.join(output_path, "tmp_tree.newick")
    outfile = open(tmp_tree_path, 'w')
    outfile.write(lines[i])
    outfile.close()
    results_all_rootings_ml = output_path + "/" + str(i) + "/all_rootings_ml_output"
    if os.path.isdir(results_all_rootings_ml):
      shutil.rmtree(results_all_rootings_ml)
    os.makedirs(results_all_rootings_ml)
    mptp_launcher.launch_mptp_all_rootings(tmp_tree_path, results_all_rootings_ml + "/output.txt")
    
    min_s, max_s, median_s = get_all_rootings_counts(results_all_rootings_ml + "/output.txt")
    min_species.append(min_s)
    max_species.append(max_s)
    median_species.append(median_s)

    os.remove(tmp_tree_path)
  summarize_species_all_rootings(len(lines), min_species, max_species, median_species, summary_outpath)

def run_mptp_all_rootings_on_trees_one_histogram(treesfile: str, output_path: str, summary_outpath: str) -> None:
  # This always uses vanilla mptp and never uses mptp_fix!
  lines = open(treesfile).readlines()
  species = Counter()
  util.mkdirp(output_path)
  for i in range(len(lines)):
    tmp_tree_path = os.path.join(output_path, "tmp_tree.newick")
    outfile = open(tmp_tree_path, 'w')
    outfile.write(lines[i])
    outfile.close()
    results_all_rootings_ml = output_path + "/" + str(i) + "/all_rootings_ml_output"
    if os.path.isdir(results_all_rootings_ml):
      shutil.rmtree(results_all_rootings_ml)
    os.makedirs(results_all_rootings_ml)
    mptp_launcher.launch_mptp_all_rootings(tmp_tree_path, results_all_rootings_ml + "/output.txt")
    
    species = get_all_rootings_counts_one_histogram(results_all_rootings_ml + "/output.txt", species)

    os.remove(tmp_tree_path)
  summarize_species_all_rootings_one_histogram(len(lines), species, summary_outpath)


if __name__ == "__main__":
  paths = common.Paths( sys.argv )
  run_mptp_on_trees(paths.raxml_credible_ml_trees, paths.mptp_output, paths.mptp_output_csv, paths.mptp_output_summary, mptp_fix = False)
  run_mptp_all_rootings_on_trees(paths.raxml_credible_ml_trees, paths.mptp_output, paths.mptp_output_summary_all_rootings)
  run_mptp_all_rootings_on_trees_one_histogram(paths.raxml_credible_ml_trees, paths.mptp_output, paths.mptp_output_summary_all_rootings_one_histogram)
