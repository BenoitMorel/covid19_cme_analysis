import os
import sys
import shutil
import subprocess

import util
import common

def iqtree_tests(alignment, model, trees, tree, runs_dir):
  prefix = os.path.join(runs_dir, "iqtree_tests")
  cmd = []
  cmd.append(common.iqtree)
  cmd.append("-blmin")
  cmd.append(common.raxml_min_bl)
  cmd.append("-s")
  cmd.append(alignment)
  cmd.append("-m")
  cmd.append(model)
  cmd.append("-pre")
  cmd.append(prefix)
  cmd.append("-redo")
  cmd.append("-z")
  cmd.append(trees)
  cmd.append("-te")
  cmd.append(tree)
  cmd.append("-n")
  cmd.append("0")
  cmd.append("-zb")
  cmd.append("10000")
  cmd.append("-zw")
  cmd.append("-au")
  cmd.append("-nt")
  cmd.append(str(common.iqtree_threads))
  logs = subprocess.check_output(cmd)
  ll = util.find_string_between(logs, "BEST SCORE FOUND : ", "\n")
  return float(ll)

def perform_all_tests(paths):  
  iqtree_dir = os.path.join(paths.runs_dir, "iqtree_tests")
  util.mkdirp(iqtree_dir)
  iqtree_ll = iqtree_tests(paths.alignment, common.subst_model, paths.raxml_all_ml_trees, paths.raxml_best_tree, iqtree_dir)
  raxml_ll = float(open(paths.raxml_all_ml_trees_ll).readline().split(" ")[0])
  with open(paths.raxml_iqtree_ll, "w") as writer:
    writer.write("# this file contains the likelihood of the best tree at the end of the raxml-ng run, and an evaluation of likelihood of the same tree  with iqtree (with model optimization)\n")
    writer.write("raxml_ll=" + str(raxml_ll) + "\n")
    writer.write("iqtree_ll=" + str(iqtree_ll) + "\n")


