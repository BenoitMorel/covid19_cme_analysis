import os
import sys
import shutil
import subprocess

import common
import util

def remove_duplicates(input_msa, outgroup_spec, output_msa, output_json, output_outgroup_msa):
  util.clean_file(output_msa)
  util.clean_file(output_json)
  util.clean_file(output_outgroup_msa)
  # <input-msa> <outgroup-names-file> <output-fasta> <output-json> <outgroup-output-fasta>
  cmd = []
  cmd.append(common.genesis_reduce_duplicates)
  cmd.append(input_msa)
  cmd.append(outgroup_spec)
  cmd.append(output_msa)
  cmd.append(output_json)
  cmd.append(output_outgroup_msa)
  subprocess.check_call(cmd)

if (__name__ == "__main__"):
  if (len(sys.argv) != 6):
    print("Syntax: input_msa outgroup_spec output_msa output_json output_outgroup_msa")
    sys.exit(1)
  input_msa = sys.argv[1]
  outgroup_spec = sys.argv[2]
  output_msa = sys.argv[3]
  output_json = sys.argv[4]
  output_outgroup_msa = sys.argv[5]
  remove_duplicates(input_msa, output_msa, output_json)

