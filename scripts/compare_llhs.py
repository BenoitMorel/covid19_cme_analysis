import os
import sys
import shutil
import subprocess
import multiprocessing as mp

import util
import common

def iqtree_eval(alignment, model, tree, prefix):
  cmd = []
  cmd.append(common.iqtree)
  cmd.append("-blmin") # Minimum branch length
  cmd.append(common.raxml_min_bl)
  cmd.append("-s")
  cmd.append(alignment)
  cmd.append("-m")
  cmd.append(model)
  cmd.append("-pre")
  cmd.append(prefix)
  cmd.append("-redo")
  cmd.append("-z") # The tree to be evaluated
  cmd.append(tree)
  cmd.append("-te") # Thre tree on which to perform model optimization
  cmd.append(tree)
  cmd.append("-nt")
  cmd.append("1")
  logs = subprocess.check_output(cmd, encoding='utf-8')
  ll = util.find_string_between(logs, "BEST SCORE FOUND : ", "\n")
  return float(ll)

def evaluate_all_trees(paths):
  """
  This will evaluate all given trees with the given model description.
  For each tree, the model and branch lengths will be optimized while
  fixing the topology.
  This contrasts iqtree_tests, as a model optimization is performed
  for each treee separately.
  """
  iqtree_eval_dir = os.path.join(paths.runs_dir, 'iqtree_eval')
  util.mkdirp(iqtree_eval_dir)

  print('Loading RAxML-ng LLHs... ', end = '')
  raxml_lls = []
  with open(paths.raxml_all_ml_trees_ll) as reader:
    for line in reader:
      raxml_lls.append(float(line.split(' ')[0]))
  print('done.')

  print('Evaluating trees with iqtree (including model & brlen optimization)... ', end = '')
  tree_files = []
  with open(paths.raxml_all_ml_trees) as trees_file:
    for i, tree_str in enumerate(trees_file):
      # Write a separate newick file for this tree
      tree_file_name = os.path.join(iqtree_eval_dir, 'tree_%d.newick' % i)
      with open(tree_file_name, 'w') as tree_file:
        tree_file.write(tree_str)
      tree_files.append(tree_file_name)

  # Evaluate trees with model & brlen optimization
  pool = mp.Pool(common.available_cores)
  iqtree_lls = pool.starmap(iqtree_eval,
    [(paths.alignment, common.subst_model, tree_file_name, tree_file_name)
      for tree_file_name in tree_files])
  print('done')

  with open(paths.raxml_iqtree_ll_all, "w") as writer:
    writer.write('# this file contains the likelihood of all ML trees at the end of the raxml-ng run as\n')
    writer.write('# well as the likelihood as evaluated by iqtree (with model & brlen optimization under\n')
    writer.write('# fixed tree topology\n')
    writer.write('raxml_ll,iqtree_ll\n')
    for raxml_ll, iqtree_ll in zip(raxml_lls, iqtree_lls):
      writer.write('%.3f,%.3f\n' % (raxml_ll, iqtree_ll))
