import os
import sys
import shutil
import subprocess

import common
import util

def reattach_duplicates(input_newick, output_newick, duplicates_json):
  util.clean_file(output_newick)
  cmd = []
  cmd.append(common.genesis_reattach_duplicates)
  cmd.append(input_newick)
  cmd.append(output_newick)
  cmd.append(duplicates_json)
  subprocess.check_call(cmd)
  

if (__name__ == "__main__"):
  if (len(sys.argv) != 3):
    print("Syntax: input_msa input_newick")
    sys.exit(1)
  input_msa = sys.argv[1]
  input_newick = sys.argv[2]
  reattach_duplicates(input_msa, input_newick)


