import os
import sys
import launcher
import common
import subprocess

def launch_mptp_mcmc(tree, output):
  cmd = []
  cmd.append(common.mptp)
  cmd.append("--mcmc")
  cmd.append("50000000")
  cmd.append("--multi")
  cmd.append("--mcmc_sample")
  cmd.append("1000000")
  cmd.append("--mcmc_burnin")
  cmd.append("1000000")
  cmd.append("--tree_file")
  cmd.append(tree)
  cmd.append("--output_file")
  cmd.append(output)
  subprocess.check_call(cmd)

def launch_mptp(tree, output):
  cmd = []
  cmd.append(common.mptp)
  cmd.append("--ml")
  cmd.append("--tree_file")
  cmd.append(tree)
  cmd.append("--output_file")
  cmd.append(output)
  subprocess.check_call(cmd)



