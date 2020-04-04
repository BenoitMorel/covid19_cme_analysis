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
  
def get_rf_distance(tree1, tree2, empty_dir):  
  trees = os.path.join(empty_dir, "trees.txt")
  with open(trees, "w") as writer:
    writer.write(open(tree1).read())
    writer.write("\n")
    writer.write(open(tree2).read())
  cmd = []
  cmd.append(common.raxml)
  cmd.append("--rfdist")
  cmd.append(trees)
  logs = subprocess.check_output(cmd)
  rf = util.find_string_between(logs, "Average relative RF distance in this tree set: ", "\n")
  print(logs)
  print("finish implementing this!")
  return float(rf)


