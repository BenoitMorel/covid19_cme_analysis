import os
import sys
import launcher
import common
import subprocess

def launch_mptp_mcmc_internal(tree, output, use_fix):
  cmd = []
  if not use_fix:
    cmd.append(common.mptp)
  else:
    cmd.append(common.mptp_fix)
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

def launch_mptp_internal(tree, output, use_fix):
  cmd = []
  if not use_fix:
    cmd.append(common.mptp)
  else:
    cmd.append(common.mptp_fix)
  cmd.append("--ml")
  cmd.append("--tree_file")
  cmd.append(tree)
  cmd.append("--output_file")
  cmd.append(output)
  subprocess.check_call(cmd)

def launch_mptp_mcmc(tree, output):
  launch_mptp_mcmc_internal(tree, output, False)

def launch_mptp_mcmc_fixed(tree, output):
  launch_mptp_mcmc_internal(tree, output, True)

def launch_mptp(tree, output):
  launch_mptp_internal(tree, output, False)

def launch_mptp_fixed(tree, output):
  launch_mptp_internal(tree, output, True)

def launch_mptp_all_rootings(tree, output):
  cmd = []
  cmd.append(common.genesis_mptp_all_rootings)
  cmd.append(tree)
  cmd.append(output)
  subprocess.check_call(cmd)
