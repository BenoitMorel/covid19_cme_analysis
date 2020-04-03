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

  rf_distance.export_pairwise_rf_distance(paths.raxml_all_ml_trees, paths.raxml_all_ml_trees_rf_distances, paths.raxml_all_ml_trees_rf_logs)
  

  iqtree_dir = os.path.join(paths.runs_dir, "iqtree_runs")
  util.mkdirp(iqtree_dir)
  iqtree_ll = iqtree_tests.eval_ll(paths.alignment, common.subst_model, paths.raxml_all_ml_trees, iqtree_dir)
  raxml_ll = float(open(paths.raxml_all_ml_trees_ll).readline().split(" ")[0])
  with open(paths.raxml_iqtree_ll, "w") as writer:
    writer.write("# this file contains the likelihood of the best tree at the end of the raxml-ng run, and an evaluation of likelihood of the same tree  with iqtree (with model optimization)\n")
    writer.write("raxml_ll=" + str(raxml_ll) + "\n")
    writer.write("iqtree_ll=" + str(iqtree_ll) + "\n")

