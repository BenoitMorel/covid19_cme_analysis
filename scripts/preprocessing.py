import os
import sys
import shutil
import subprocess

import common
import util

def trim_separate_align(input_fasta, mode, runsdir, version_dir):
  util.expect_file_exists( input_fasta )
  util.clean_dir( runsdir )
  util.mkdirp( runsdir )

  cmd = []
  cmd.append(common.preanalysis1)
  cmd.append(input_fasta)
  cmd.append(mode)
  cmd.append(common.scripts_dir)
  cmd.append(common.mafft)
  cmd.append(common.outgroup_spec)
  cmd.append(version_dir)
  cmd.append(str(common.available_cores))
  print(" ".join(cmd))
  subprocess.check_call(cmd, cwd=runsdir)

def remove_duplicates(input_msa, output_msa, output_json):
  util.expect_file_exists( input_msa )

  util.clean_file(output_msa)
  util.clean_file(output_json)

  cmd = []
  cmd.append(common.genesis_reduce_duplicates)
  cmd.append(input_msa)
  cmd.append(output_msa)
  cmd.append(output_json)
  subprocess.check_call(cmd)

if (__name__ == "__main__"):
  if (len(sys.argv) != 4):
    print("Syntax: input_msa output_msa output_json")
    sys.exit(1)
  input_msa = sys.argv[1]
  output_msa = sys.argv[2]
  output_json = sys.argv[3]
  remove_duplicates(input_msa, output_msa, output_json)

