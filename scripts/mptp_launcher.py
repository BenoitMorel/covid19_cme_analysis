import os
import sys
import launcher
import common
import subprocess

def launch_mptp(tree, output):
  cmd = []
  cmd.append(common.mptp)
  cmd.append("--ml")
  cmd.append("--tree_file")
  cmd.append(tree)
  cmd.append("--output_file")
  cmd.append(output)
  subprocess.check_call(cmd)



