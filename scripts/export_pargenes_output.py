import os
import sys
import shutil

import util
import common
import reattach_duplicates

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
  reattach_duplicates.reattach_duplicates(src, paths.raxml_best_tree_with_duplicate, paths.duplicates_json)
  
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




