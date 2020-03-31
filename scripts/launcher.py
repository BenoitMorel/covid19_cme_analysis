import os
import datetime
import sys
import subprocess
import shutil

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
  historic = "historic.txt"
  out = open(historic, "a+")
  subprocess.check_call(command, stdout = out)
  out.write("Submission script in " + submitfile + "\n")
  out.write("Output in " + logfile + "\n")
  print(open(historic).readlines()[-3][:-1])
  print(open(historic).readlines()[-2][:-1])
  print(open(historic).readlines()[-1][:-1])
  out.write("\n")

def submit_normal(cmd):
  subprocess.check_call(cmd)

def is_slurm():
  try:
    subprocess.call(["sbatch", "-V"])
  except:
    return False
  return True

def submit(prefix, cmd, cores, debug = False):
  if (is_slurm()):
    submit_haswell(prefix, cmd, cores, debug)
  else:
    submit_normal(cmd)

