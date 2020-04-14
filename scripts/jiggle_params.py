import os
import sys
import shutil
import subprocess
import multiprocessing as mp
import re

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

def raxml_eval(alignment, model, tree_file, prefix):
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
  cmd.append("-z") # The tree to be evaluated
  cmd.append(tree_file)
  cmd.append("-T")
  cmd.append(str(common.raxml_eval_cores))
  cmd.append('-p') # Random seed
  cmd.append('42')
  cmd.append('-f')
  cmd.append('n') # Optimize model and brlen and compute loglh
  logs = subprocess.check_output(cmd, encoding='utf-8')
  pattern = re.compile('^Tree \d+ Likelihood (-\d+\.\d+) Tree-Length')
  lls = [
    float(match.group(1))
    for match in
      [re.search(pattern, hay) for hay in logs.split('\n')]
    if match
  ]
  return lls

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
  cmd.append(str(common.raxmlng_eval_cores))
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

  print('Jiggling some parameters to check how the LLH change on THE maximum likelihood tree', end = '')
  params_sets = []
  for blmin in ('1e-1', '1e-2', '1e-3', '1e-4', '1e-5', '1e-6', '1e-7', '1e-8', '1e-9', '1e-10'):
    params_sets.append((paths.alignment, common.subst_model, blmin, '100', 'nr_safe', '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blmin_%s' % blmin)))

  for blmax in ('1e1', '1e2', '1e3', '1e4', '1e5', '1e6'):
    params_sets.append((paths.alignment, common.subst_model, '1e-6', blmax, 'nr_safe', '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blmax_%s' % blmax)))

  for blopt in ('nr_safe', 'nr_fast', 'nr_oldfast', 'nr_oldsafe'):
    params_sets.append((paths.alignment, common.subst_model, '1e-6', '100', blopt, '0.1',
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'blopt_%s' % blopt)))

  for lh_epsilon in ('10', '1', '0.1', '0.01', '0.001', '0.0001'):
    params_sets.append((paths.alignment, common.subst_model, '1e-6', '100', 'nr_safe', lh_epsilon,
      paths.raxml_best_tree, os.path.join(jiggle_params_dir, 'lh_epsilon_%s' % lh_epsilon)))

  pool = mp.Pool(common.available_cores)
  llhs = pool.starmap(raxmlng_eval, params_sets)
  print('done')

  with open(paths.param_jiggle_llhs, "w") as writer:
    writer.write('blmin,blmsc,blopt,lh_epsilon,llh\n')
    for llh, params in zip(llhs, params_sets):
      if llh is None:
        llh = "NA"
      writer.write('%s,%s,%s,%s,%s\n' % (params[2], params[3], params[4], params[5], llh))
