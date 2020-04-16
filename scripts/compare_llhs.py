import os
import sys
import shutil
import subprocess
import multiprocessing as mp
import re

import util
import common

def iqtree_eval(alignment, model, tree, prefix, gmedian = False):
  cmd = []
  cmd.append(common.iqtree)
  cmd.append("-blmin") # Minimum branch length
  cmd.append(common.raxml_min_bl)
  cmd.append("-s")
  cmd.append(alignment)
  cmd.append("-m")
  cmd.append(model)
  if gmedian:
      cmd.append("-gmedian")
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

def raxml_eval_all(alignment, model, trees_file, prefix):
  os.chdir(os.path.dirname(prefix))
  cmd = []
  cmd.append(common.old_raxml)
  cmd.append("-s")
  cmd.append(alignment)
  cmd.append("-m")
  cmd.append(model)
  cmd.append("-n")
  cmd.append(os.path.basename(prefix))
  cmd.append("-redo")
  cmd.append("-z") # The trees to be evaluated
  cmd.append(trees_file)
  cmd.append("-T")
  cmd.append(str(common.raxml_eval_cores))
  cmd.append('-p') # Random seed
  cmd.append('42')
  cmd.append('-f')
  cmd.append('N') # Optimize model and brlen per tree and compute loglh
  logs = subprocess.check_output(cmd, encoding='utf-8')
  pattern = re.compile('^Tree \d+ Likelihood (-\d+\.\d+) Tree-Length')
  lls = [
    float(match.group(1))
    for match in
      [re.search(pattern, hay) for hay in logs.split('\n')]
    if match
  ]
  return lls

def raxmlng_eval_all(alignment, model, trees_file, prefix):
  cmd = []
  cmd.append(common.raxml)
  cmd.append('--evaluate')
  cmd.append('--msa')
  cmd.append(alignment)
  cmd.append('--model')
  cmd.append(model)
  cmd.append('--tree')
  cmd.append(trees_file)
  cmd.append('--prefix')
  cmd.append(prefix)
  cmd.append('--threads')
  cmd.append(str(common.raxmlng_eval_cores))
  cmd.append('--blopt')
  cmd.append('nr_safe')
  cmd.append('--redo')
  logs = subprocess.check_output(cmd, encoding = 'utf-8')
  pattern = re.compile('^\[\d+:\d+:\d+\] Tree #\d+, final logLikelihood: (-\d+\.\d+)$')
  lls = [
    float(match.group(1))
    for match in
      [re.search(pattern, hay) for hay in logs.split('\n')]
    if match
  ]
  return lls

def evaluate_all_trees(paths):
  """
  This will evaluate all given trees with the given model description.
  For each tree, the model and branch lengths will be optimized while
  fixing the topology.
  This contrasts iqtree_tests, as a model optimization is performed
  for each treee separately.
  """
  iqtree_eval_dir_model = os.path.join(paths.runs_dir, 'iqtree_eval_model')
  util.mkdirp(iqtree_eval_dir_model)
  iqtree_eval_dir_gamma = os.path.join(paths.runs_dir, 'iqtree_eval_gamma')
  util.mkdirp(iqtree_eval_dir_gamma)
  raxml_eval_dir_gamma = os.path.join(paths.runs_dir, 'raxml_eval_gamma')
  util.mkdirp(raxml_eval_dir_gamma)
  raxmlng_eval_dir_gamma = os.path.join(paths.runs_dir, 'raxmlng_eval_gamma')
  util.mkdirp(raxmlng_eval_dir_gamma)
  iqtree_eval_dir_gamma_median = os.path.join(paths.runs_dir, 'iqtree_eval_gamma_median')
  util.mkdirp(iqtree_eval_dir_gamma_median)
  raxmlng_eval_dir_gamma_median = os.path.join(paths.runs_dir, 'raxmlng_eval_gamma_median')
  util.mkdirp(raxmlng_eval_dir_gamma_median)

  print('Comparing LLHs for model %s' % common.subst_model)
  print('Loading RAxML-ng LLHs... ', end = '')
  raxmlng_lls = []
  with open(paths.raxml_all_ml_trees_ll) as reader:
    for line in reader:
      raxmlng_lls.append(float(line.split(' ')[0]))
  print('done.')

  print('Evaluating trees with iqtree (including model & brlen optimization)... ', end = '')
  tree_files = []
  with open(paths.raxml_all_ml_trees) as trees_file:
    for i, tree_str in enumerate(trees_file):
      # Write a separate newick file for this tree
      tree_file_name = os.path.join(iqtree_eval_dir_model, 'tree_%d.newick' % i)
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
    writer.write('raxmlng,iqtree\n')
    for raxmlng_ll, iqtree_ll in zip(raxmlng_lls, iqtree_lls):
      writer.write('%.3f,%.3f\n' % (raxmlng_ll, iqtree_ll))

  # Evaluate using GTR+GAMMA Model
  print('Comparing LLHs for GTR+GAMMA model')

  print('Evaluating trees with RAxML-ng (including model & brlen optimization)... ', end = '')
  raxmlng_lls = raxmlng_eval_all(paths.alignment, 'GTR+FO+G', paths.raxml_all_ml_trees, os.path.join(raxmlng_eval_dir_gamma, 'eval'))
  print('done')

  print('Evaluating trees with iqtree (including model & brlen optimization)... ', end = '')
  iqtree_lls = pool.starmap(iqtree_eval,
    [(paths.alignment, 'GTR+FO+G', tree_file_name, tree_file_name.replace(iqtree_eval_dir_model, iqtree_eval_dir_gamma))
      for tree_file_name in tree_files])
  print('done')

  print('Evaluating trees with RAxML (including model & brlen optimization)... ', end = '')
  raxml_lls = raxml_eval_all(paths.alignment, 'GTRGAMMAX', paths.raxml_all_ml_trees, os.path.join(raxmlng_eval_dir_gamma, 'eval'))
  print('done')

  with open(paths.gamma_ll_all, "w") as writer:
    writer.write('# this file contains the likelihood of all ML trees optimized and evaluated\n')
    writer.write('# under GTR+F0+G and fixed tree topology\n')
    writer.write('raxmlng,iqtree,raxml\n')
    for raxmlng_ll, iqtree_ll, raxml_ll in zip(raxmlng_lls, iqtree_lls, raxml_lls):
      writer.write('%.3f,%.3f,%.3f\n' % (raxmlng_ll, iqtree_ll, raxml_ll))

  # Evaluate using GTR+GAMMA Model with median rates
  print('Comparing LLHs for GTR+GAMMA model with median rates')

  print('Evaluating trees with RAxML-ng (including model & brlen optimization)... ', end = '')
  raxmlng_lls = raxmlng_eval_all(paths.alignment, 'GTR+FO+GA', paths.raxml_all_ml_trees, os.path.join(raxmlng_eval_dir_gamma_median, 'eval'))
  print('done')

  print('Evaluating trees with iqtree (including model & brlen optimization)... ', end = '')
  iqtree_lls = pool.starmap(iqtree_eval,
    [(paths.alignment, 'GTR+FO+G', tree_file_name, tree_file_name.replace(iqtree_eval_dir_model, iqtree_eval_dir_gamma_median), True)
      for tree_file_name in tree_files])
  print('done')

  with open(paths.gamma_median_ll_all, "w") as writer:
    writer.write('# this file contains the likelihood of all ML trees optimized and evaluated\n')
    writer.write('# under GTR+F0+GA and fixed tree topology\n')
    writer.write('raxmlng,iqtree\n')
    for raxmlng_ll, iqtree_ll  in zip(raxmlng_lls, iqtree_lls):
      writer.write('%.3f,%.3f\n' % (raxmlng_ll, iqtree_ll))

