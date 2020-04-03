import os
import sys
import shutil
import subprocess

import util
import common

def eval_ll(alignment, model, tree, runs_dir):
  prefix = os.path.join(runs_dir, "eval_ll")
  cmd = []
  cmd.append(common.iqtree)
  cmd.append("-blmin")
  cmd.append(common.raxml_min_bl)
  cmd.append("-s")
  cmd.append(alignment)
  cmd.append("-m")
  cmd.append(model)
  cmd.append("-z")
  cmd.append(tree)
  cmd.append("-pre")
  cmd.append(prefix)
  cmd.append("-redo")
  cmd.append("-te")
  cmd.append(tree)
  cmd.append("-n")
  cmd.append("0")
  cmd.append("-zb")
  cmd.append("1000")
  cmd.append("-zw")
  cmd.append("-au")
  logs = subprocess.check_output(cmd)
  print(logs)
  ll = util.find_string_between(logs, "BEST SCORE FOUND : ", "\n")
  return float(ll)

  

