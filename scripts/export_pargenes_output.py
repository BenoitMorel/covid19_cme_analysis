import os
import sys
import shutil

import util
import common

def export(pargenes_run_dir, version):
  print("Pargenes run dir: " + pargenes_run_dir)
  pargenes_output = os.path.join(pargenes_run_dir, "pargenes_output")
  
# export tree with support values
  src = os.path.join(pargenes_output, "supports_run", "results", "ali_fasta.support.raxml.support")
  dest = util.versioned_path(version, common.raxml_best_tree)
  shutil.copy(src, dest)

# export best ml tree
  ml_run_dir = os.path.join(pargenes_output, "mlsearch_run", "results", "ali_fasta")
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
  src = os.path.join(pargenes_output, "concatenated_bootstraps", "ali_fasta.bs")
  dest = util.versioned_path(version, common.raxml_bootstrap_trees)
  shutil.copy(src, dest)



