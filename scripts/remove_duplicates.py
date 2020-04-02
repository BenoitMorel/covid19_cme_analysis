import ete3
import os
import sys
import shutil
import subprocess

import common
import util

def remove_duplicates(input_msa, output_msa):
  if (not input_msa.endswith(".fasta")):
    print("Error, remove_duplicates only support files that end with .fasta")
    sys.exit(1)
  genesis_output = input_msa.replace(".fasta", ".reduced.fasta")
  genesis_json_output = input_msa.replace(".fasta", ".reduced.json")
  util.clean_file(genesis_output)
  util.clean_file(genesis_json_output)
  cmd = []
  cmd.append(common.genesis_reduce_duplicates)
  cmd.append(input_msa)
  subprocess.check_call(cmd)
  shutil.move(genesis_output, output_msa)
  

if (__name__ == "__main__"):
  if (len(sys.argv) != 3):
    print("Syntax: input_msa output_msa")
    sys.exit(1)
  input_msa = sys.argv[1]
  output_msa = sys.argv[2]
  remove_duplicates(input_msa, output_msa)

