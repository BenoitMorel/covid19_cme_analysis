import os
import sys
import shutil

import util
import common
import reattach_duplicates
import rf_distance
import iqtree_tests

def export(pargenes_run_dir, paths):
  print("Pargenes run dir: " + pargenes_run_dir)
  pargenes_output = os.path.join(pargenes_run_dir, "pargenes_output")
  ml_run_dir = os.path.join(pargenes_output, "mlsearch_run", "results", "ali_fasta")

# export best ml tree (with support values if existing)
  src = ""
  if (common.pargenes_bs_trees > 0):
    src = os.path.join(pargenes_output, "supports_run", "results", "ali_fasta.support.raxml.support")
  else:
    src = os.path.join(ml_run_dir, "ali_fasta.raxml.bestTree")
  shutil.copy(src, paths.raxml_best_tree)

# export best tree with duplicates reattached
  reattach_duplicates.reattach_duplicates(src, paths.raxml_best_tree_with_duplicate, paths.duplicates_json)
  
# export best tree with TBE values
  if (common.pargenes_bs_trees > 0):
    src = os.path.join(pargenes_output, "supports_run", "results", "ali_fasta.support.tbe.raxml.support")
    shutil.copy(src, paths.raxml_best_tree_tbe)

# export best ml model
  src = os.path.join(ml_run_dir, "ali_fasta.raxml.bestModel")
  shutil.copy(src, paths.raxml_best_model)

# export all ml trees
  src = os.path.join(ml_run_dir, "sorted_ml_trees.newick")
  shutil.copy(src, paths.raxml_all_ml_trees)
  src = os.path.join(ml_run_dir, "sorted_ml_trees_ll.newick")
  shutil.copy(src, paths.raxml_all_ml_trees_ll)

# export bootstrap trees
  if (common.pargenes_bs_trees > 0):
    src = os.path.join(pargenes_output, "concatenated_bootstraps", "ali_fasta.bs")
    shutil.copy(src, paths.raxml_bootstrap_trees)

  av_pairwise_rf_distance = rf_distance.get_export_pairwise_rf_distance(paths.raxml_all_ml_trees, paths.raxml_all_ml_trees_rf_distances, paths.raxml_all_ml_trees_rf_logs)
  toprint0 = "Average pairwise RF distance between all ML trees: " + str(av_pairwise_rf_distance)
  print(av_pairwise_rf_distance) 

# compute RF distance between starting and ML trees for the best run
  print("Computing rf distances between parsimony and ML trees...")
  rf_dir = os.path.join(paths.runs_dir, "rfdistances")
  util.clean_dir(rf_dir)
  util.mkdirp(rf_dir)
  prefix = os.path.join(rf_dir, "ml")
  tree1 = os.path.join(ml_run_dir, "ali_fasta.raxml.bestTree")
  tree2 = os.path.join(ml_run_dir, "ali_fasta.raxml.startTree")
  rf = rf_distance.get_rf_distance(tree1, tree2, prefix)
  toprint1 = "RF distance between the best ML tree and its starting tree: " + str(rf)
  all_runs_dir = os.path.join(ml_run_dir, "multiple_runs")
  
  sum_rf = 0.0
  deno_rf = 0.0
  for run in os.listdir(all_runs_dir):
    run_dir = os.path.join(all_runs_dir, run)
    prefix = os.path.join(rf_dir, run)
    tree1 = os.path.join(run_dir, "ali_fasta.raxml.bestTree")
    tree2 = os.path.join(run_dir, "ali_fasta.raxml.startTree")
    rf = rf_distance.get_rf_distance(tree1, tree2, prefix)
    sum_rf += rf
    deno_rf += 1.0
  av_rf = sum_rf / deno_rf
  toprint2 = "Average (over all the " + str(deno_rf) + " runs) RF distance between start and ML trees: " + str(av_rf)
  print(toprint0)
  print(toprint1)
  print(toprint2)
  with open(paths.rf_distance_report, "w") as writer:
    writer.write(toprint0 + "\n")
    writer.write(toprint1 + "\n")
    writer.write(toprint2)

