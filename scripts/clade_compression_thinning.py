import shutil
import sys
import os
import subprocess
import common
import util

def clade_compression_thinning(paths, input_tree_filename, input_alignment, taxa_number, output_alignment):
  util.make_path_clean(paths.cc_thinning_runs_dir)
  prefix = os.path.join(paths.cc_thinning_runs_dir, "cc_thinning")
  command = []

  command.append(common.genesis_clade_compression)
  command.append(input_tree_filename)
  command.append(input_alignment)
  command.append(str(taxa_number))
  command.append(str(10000))
  command.append(prefix)
  print(" ".join(command))
  subprocess.check_call(command)
 
  shutil.move(prefix + "_pruned_alignment.fasta", output_alignment)
  print("Clade-compression thinned alignment ouputed in " + output_alignment) 


