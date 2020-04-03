import os
import sys
import launcher
import common
import subprocess
import util

def launch_epa(tree, modelfile, ref_msa, query_msa, out_dir, thorough=True):
  util.clean_dir(out_dir)
  util.make_path(out_dir)

  cmd = []
  cmd.append(common.epa)
  cmd.append("--tree")
  cmd.append(tree)
  cmd.append("--model")
  cmd.append(modelfile)
  cmd.append("--msa")
  cmd.append(ref_msa)
  cmd.append("--query")
  cmd.append(query_msa)
  cmd.append("--threads")
  cmd.append("4")
  if thorough:
  	cmd.append("--no-heur")
  cmd.append("--out-dir")
  cmd.append(out_dir)
  subprocess.check_call(cmd)



