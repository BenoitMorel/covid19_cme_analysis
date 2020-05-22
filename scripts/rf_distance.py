import os
import sys
import common
import subprocess
import util
import shutil

def get_export_pairwise_rf_distance(input_trees_file, output_distances):
  cmd = []
  tmp_prefix = input_trees_file + ".rf.tmp"
  cmd.append(common.raxml)
  cmd.append("--rfdist")
  cmd.append(input_trees_file)
  cmd.append("--prefix")
  cmd.append(tmp_prefix)
  logs = subprocess.check_output(cmd, encoding='utf-8')
  shutil.move(tmp_prefix + ".raxml.rfDistances", output_distances)
  rf = util.find_string_between(logs, "Average relative RF distance in this tree set: ", "\n")
  return rf 

def get_rf_distance(tree1, tree2, prefix):  
  trees = prefix +  "_trees.txt"
  with open(trees, "w") as writer:
    writer.write(open(tree1).read())
    writer.write("\n")
    writer.write(open(tree2).read())
  cmd = []
  cmd.append(common.raxml)
  cmd.append("--rfdist")
  cmd.append(trees)
  logs = subprocess.check_output(cmd, encoding='utf-8')
  rf = util.find_string_between(logs, "Average relative RF distance in this tree set: ", "\n")
  return float(rf)


