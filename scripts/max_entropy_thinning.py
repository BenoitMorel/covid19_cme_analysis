import shutil
import sys
import os
import subprocess
import common
import util

def max_entropy_thinning(paths, input_alignment, taxa_number, output_alignment):
  util.make_path_clean(paths.me_thinning_runs_dir)
  prefix = os.path.join(paths.me_thinning_runs_dir, "me_thinning")
  command = []
  command.append(common.genesis_max_entropy)
  command.append(input_alignment)
  command.append(str(taxa_number))
  command.append(prefix)
  print(" ".join(command))
  subprocess.check_call(command)
  shutil.move(prefix + "_pruned_alignment.fasta", output_alignment)



