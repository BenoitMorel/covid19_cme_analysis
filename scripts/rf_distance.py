import os
import sys
import common
import subprocess
import util
import shutil

def export_pairwise_rf_distance(input_trees_file, output_distances, output_summary):
  cmd = []
  tmp_prefix = input_trees_file + ".rf.tmp"
  cmd.append(common.raxml)
  cmd.append("--rfdist")
  cmd.append(input_trees_file)
  cmd.append("--prefix")
  cmd.append(tmp_prefix)
  logs = subprocess.check_output(cmd)
  shutil.move(tmp_prefix + ".raxml.rfDistances", output_distances)
  shutil.move(tmp_prefix + ".raxml.log", output_summary)
  
  
