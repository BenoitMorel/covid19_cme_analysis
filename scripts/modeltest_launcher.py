import os
import sys
import launcher
import common


def launch_modeltest(alignment, output_dir, seed, cores = 16, debug = False):
  try:
    os.mkdir(output_dir)
  except:
    pass
  cmd = []
  prefix = os.path.join(output_dir, "modeltest" ) 
  prefix += "_seed" + str(seed)
  cmd.append("mpiexec")
  cmd.append("-np")
  cmd.append(str(cores))
  cmd.append(common.modeltest)
  cmd.append("-i")
  cmd.append(alignment)
  cmd.append("-t")
  cmd.append("mp")
  cmd.append("-o")
  cmd.append(prefix)
  cmd.append("--force")
  cmd.append("-h")
  cmd.append("uigfr")
  launcher.submit_haswell(prefix, cmd, cores, debug) 



