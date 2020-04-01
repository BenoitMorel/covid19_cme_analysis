import os
import datetime
import sys
import subprocess
import shutil
import util

def submit_haswell(prefix, cmd, cores = 16, debug =  False):
  cores = int(cores)
  nodes = str((int(cores) - 1) // 16 + 1)
  logfile = os.path.join(prefix + "_haswelllogs.out")
  submitfile = os.path.join(prefix + "_haswellsubmit.sh")
  with open(submitfile, "w") as f:
    f.write("#!/bin/bash\n")
    f.write("#SBATCH -o " + logfile + "\n")
    f.write("#SBATCH -B 2:8:1\n")
    f.write("#SBATCH -N " + str(nodes) + "\n")
    f.write("#SBATCH -n " + str(cores) + "\n")
    f.write("#SBATCH --threads-per-core=1\n")
    f.write("#SBATCH --cpus-per-task=1\n")
    f.write("#SBATCH --hint=compute_bound\n")
    if (debug):
      f.write("#SBATCH -t 2:00:00\n")
    else:
      f.write("#SBATCH -t 24:00:00\n")

    f.write("\n")
    f.write(" ".join(cmd))
  command = []
  command.append("sbatch")
  if (debug):
    command.append("--qos=debug")
  command.append("-s")
  command.append(submitfile)
  subprocess.check_call(command)
  print("Submission script in " + submitfile)
  print("Output in " + logfile)

def submit_normal(cmd):
  subprocess.check_call(cmd)


def submit(prefix, cmd, cores, debug = False):
  if (util.is_slurm()):
    submit_haswell(prefix, cmd, cores, debug)
  else:
    submit_normal(cmd)

