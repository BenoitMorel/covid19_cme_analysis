import os
import sys
import launcher
import common
import subprocess
import util

def launch_root_digger(tree, alignment, model, treefile, logfile, cores, factor = "1e20"):
  cmd = ["mpiexec"]
  cmd.extend(["-np", cores])
  cmd.extend([common.root_digger])
  cmd.extend(["--tree", tree])
  cmd.extend(["--msa", alignment])
  cmd.extend(["--model", model])
  cmd.extend(["--exhaustive"])
  cmd.extend(["--treefile", treefile])
  cmd.extend(["--early-stop"])
  #cmd.extend(["--verbose"])
  cmd.extend(["|", "tee", logfile])
  subprocess.check_call(cmd)
