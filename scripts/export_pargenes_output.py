import os
import sys
import shutil

import util
import common
import reattach_duplicates

def export(pargenes_run_dir, version):
  print("Pargenes run dir: " + pargenes_run_dir)
  pargenes_output = os.path.join(pargenes_run_dir, "pargenes_output")
  ml_run_dir = os.path.join(pargenes_output, "mlsearch_run", "results", "ali_fasta")
  duplicates = util.versioned_path( version, common.duplicates_json )

# export best ml tree (with support values if existing)
  src = ""
  if (common.pargenes_bs_trees > 0):
    src = os.path.join(pargenes_output, "supports_run", "results", "ali_fasta.support.raxml.support")
  else:
    src = os.path.join(ml_run_dir, "ali_fasta.raxml.bestTree")
  dest = util.versioned_path(version, common.raxml_best_tree)
  dest_dup = util.versioned_path(version, common.raxml_best_tree_with_duplicate)
  shutil.copy(src, dest)
  reattach_duplicates.reattach_duplicates(src, dest_dup, duplicates)
  
# export best ml model
  src = os.path.join(ml_run_dir, "ali_fasta.raxml.bestModel")
  dest = util.versioned_path(version, common.raxml_best_model)
  shutil.copy(src, dest)

# export all ml trees
  src = os.path.join(ml_run_dir, "sorted_ml_trees.newick")
  dest = util.versioned_path(version, common.raxml_all_ml_trees)
  shutil.copy(src, dest)
  src = os.path.join(ml_run_dir, "sorted_ml_trees_ll.newick")
  dest = util.versioned_path(version, common.raxml_all_ml_trees_ll)
  shutil.copy(src, dest)

# export bootstrap trees
  if (common.pargenes_bs_trees > 0):
    src = os.path.join(pargenes_output, "concatenated_bootstraps", "ali_fasta.bs")
    dest = util.versioned_path(version, common.raxml_bootstrap_trees)
    shutil.copy(src, dest)



