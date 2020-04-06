import os
import sys
import shutil
import subprocess

import util
import common


def build_consensus_tree(input_trees, output_tree, run_dir, mode = "MR"):
  util.mkdirp(run_dir)
  prefix = os.path.join(run_dir, "consensus_" + mode)
  cmd = []
  cmd.append(common.raxml)
  cmd.append("--consense")
  cmd.append(mode)
  cmd.append("--tree")
  cmd.append(input_trees)
  cmd.append("--prefix")
  cmd.append(prefix)
  cmd.append("--redo")
  subprocess.check_output(cmd)
  consensus = prefix + ".raxml.consensusTree" + mode
  print("Saving consensus tree to " + output_tree)
  shutil.copy(consensus, output_tree)

