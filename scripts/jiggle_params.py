import os
import sys
import shutil
import subprocess
import multiprocessing as mp
import re

import util
import common

def iqtree_eval(alignment, model, blmin, blmax, safe, lh_epsilon, tree_file, prefix):
  cmd = []
  cmd.append(common.iqtree)
  cmd.append("-blmin") # Minimum branch length
  cmd.append(blmin)
  cmd.append("-blmax")
  cmd.append(blmax)
  if safe:
    cmd.append("-safe")
  cmd.append("-me")
  cmd.append(lh_epsilon)
  cmd.append("-s")
  cmd.append(alignment)
  cmd.append("-m")
  cmd.append(model)
  cmd.append("-pre")
  cmd.append(prefix)
  cmd.append("-redo")
  cmd.append("-z") # The tree to be evaluated
  cmd.append(tree_file)
  cmd.append("-te") # Thre tree on which to perform model optimization
  cmd.append(tree_file)
  cmd.append("-nt")
  cmd.append("1")
  logs = subprocess.check_output(cmd, encoding='utf-8')
  ll = util.find_string_between(logs, "BEST SCORE FOUND : ", "\n")
  return float(ll)

def raxmlng_eval(alignment, model, blmin, blmax, blopt, lh_epsilon, tree_file, prefix):
  cmd = []
  cmd.append(common.raxml)
  cmd.append('--evaluate')
  cmd.append('--msa')
  cmd.append(alignment)
  cmd.append('--model')
  cmd.append(model)
  cmd.append('--tree')
  cmd.append(tree_file)
  cmd.append('--prefix')
  cmd.append(prefix)
  cmd.append('--threads')
  cmd.append(1)
  cmd.append('--blopt')
  cmd.append(blopt)
  cmd.append('--blmin')
  cmd.append(blmin)
  cmd.append('--blmax')
  cmd.append(blmax)
  cmd.append('--lh-epsilon')
  cmd.append(lh_epsilon)
  cmd.append('--redo')

  try:
    logs = subprocess.check_output(cmd, encoding = 'utf-8')
  except subprocess.CalledProcessError as e:
    print("command '%s' return with error (code %d): %s" % (e.cmd, e.returncode, e.output))
    return None
  else:
    ll = util.find_string_between(logs, ", final logLikelihood: ", "\n")
    return ll

def evaluate_all(paths):
  jiggle_params_dir = os.path.join(paths.runs_dir, 'jiggle_params')
  util.mkdirp(jiggle_params_dir)

  print('Jiggling some parameters to check how the LLHs change on THE maximum likelihood tree', end = '')
  raxmlng_params_sets = []
  iqtree_params_sets = []
  for blmin in ('1e-1', '1e-2', '1e-3', '1e-4', '1e-5', '1e-6', '1e-7', '1e-8', '1e-9', '1e-10'):
    raxmlng_params_sets.append((paths.alignment, common.subst_model, blmin, '100', 'nr_safe', '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blmin_%s' % blmin)))
    iqtree_params_sets.append((paths.alignment, common.subst_model, blmin, '100', True, '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blmin_%s' % blmin)))

  for blmax in ('1e1', '1e2', '1e3', '1e4', '1e5', '1e6'):
    raxmlng_params_sets.append((paths.alignment, common.subst_model, '1e-6', blmax, 'nr_safe', '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blmax_%s' % blmax)))
    iqtree_params_sets.append((paths.alignment, common.subst_model, '1e-6', blmax, True, '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blmax_%s' % blmax)))

  for blopt in ('nr_safe', 'nr_fast', 'nr_oldfast', 'nr_oldsafe'):
    raxmlng_params_sets.append((paths.alignment, common.subst_model, '1e-6', '100', blopt, '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blopt_%s' % blopt)))
  for safe in (True, False):
    iqtree_params_sets.append((paths.alignment, common.subst_model, '1e-6', '100', safe, '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blopt_%s' % str(blopt))))

  for lh_epsilon in ('10', '1', '0.1', '0.01', '0.001', '0.0001'):
    raxmlng_params_sets.append((paths.alignment, common.subst_model, '1e-6', '100', 'nr_safe', lh_epsilon,
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'lh_epsilon_%s' % lh_epsilon)))
    if float(lh_epsilon) <= 0.1: # iqtree supports only <= 0.1
      iqtree_params_sets.append((paths.alignment, common.subst_model, '1e-6', '100', True, lh_epsilon,
        paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'lh_epsilon_%s' % lh_epsilon)))

  pool = mp.Pool(common.available_cores)
  raxmlng_llhs = pool.starmap(raxmlng_eval, raxmlng_params_sets)
  iqtree_llhs = pool.starmap(iqtree_eval, iqtree_params_sets)

  with open(paths.raxmlng_param_jiggle_llhs, "w") as writer:
    writer.write('blmin,blmax,blopt,lh_epsilon,llh\n')
    for llh, params in zip(raxmlng_llhs, raxmlng_params_sets):
      if llh is None:
        llh = "NA"
      writer.write('%s,%s,%s,%s,%s\n' % (params[2], params[3], params[4], params[5], llh))

  with open(paths.iqtree_param_jiggle_llhs, "w") as writer:
    writer.write('blmin,blmax,blopt,lh_epsilon,llh\n')
    for llh, params in zip(iqtree_llhs, iqtree_params_sets):
      if llh is None:
        llh = "NA"
      writer.write('%s,%s,%s,%s,%s\n' % (params[2], params[3], params[4], params[5], llh))

  print('done')
