import os
import sys
import launcher
import common
import subprocess
import util

def launch_root_digger(tree, alignment, model, treefile, logfile, threads, factor = "1e20"):
  cmd = [common.root_digger]
  cmd.extend(["--tree", tree])
  cmd.extend(["--msa", alignment])
  cmd.extend(["--model", model])
  cmd.extend(["--threads", str(threads)])
  cmd.extend(["--exhaustive"])
  cmd.extend(["--factor", factor])
  cmd.extend(["--treefile", treefile])
  cmd.extend(["--atol", "1e-2"])
  cmd.extend(["--bfgstol", "1e-2"])
  cmd.extend(["--brtol", "1e-2"])
  #cmd.extend(["--verbose"])
  cmd.extend(["|", "tee", logfile])
  subprocess.check_call(cmd)
