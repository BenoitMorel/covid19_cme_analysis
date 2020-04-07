import os
import sys
import shutil
import subprocess

import util
import common

def iqtree_tests(alignment, model, trees, tree, runs_dir):
  prefix = os.path.join(runs_dir, "iqtree_tests")
  cmd = []
  cmd.append(common.iqtree)
  cmd.append("-blmin")
  cmd.append(common.raxml_min_bl)
  cmd.append("-s")
  cmd.append(alignment)
  cmd.append("-m")
  cmd.append(model)
  cmd.append("-pre")
  cmd.append(prefix)
  cmd.append("-redo")
  cmd.append("-z")
  cmd.append(trees)
  cmd.append("-te")
  cmd.append(tree)
  cmd.append("-n")
  cmd.append("0")
  cmd.append("-zb")
  cmd.append("10000")
  cmd.append("-zw")
  cmd.append("-au")
  cmd.append("-nt")
  cmd.append(str(common.iqtree_threads))
  logs = subprocess.check_output(cmd)
  ll = util.find_string_between(logs, "BEST SCORE FOUND : ", "\n")
  return float(ll)

def extract_tests_results(iqtree_tests_file):
  # this is a very quick and dirty implementation...
  lines = open(iqtree_tests_file).readlines()
  begin = 0
  end = 0
  for i in range(0, len(lines)):
    if (lines[i] == "USER TREES\n"):
      begin = i
    if (lines[i] == "TIME STAMP\n"):
      end = i
  res = []
  for line in lines[begin: end]:
    #if (line.startswith("Tree")):
      #res.append(line.replace("\n", ""))
    if (line.strip().split(" ")[0].isdigit()):
      res.append(line.replace("\n", ""))
  return res

"""
def get_per_test_values(iqtree_tests_file):
  iqtree_lines = extract_tests_results(iqtree_tests_file)
   
  header = iqtree_lines[0].split()
  per_test_values = {}
  tests = []
  to_skip = set(["Tree", "logL", "deltaL", "bp-RELL"])
  key_position = {}
  for i in range(0, len(header)):
    key = header[i]
    if (len(key.strip()) != 0 and not key in to_skip):
      per_test_values[key] = []
      tests.append(key)
      key_position[key] = i
  #print(tests) 
  #print(header)
  #print(key_position)
  for line in iqtree_lines[1:]:
    values = line.replace(" + ", " ").replace(" - ", " ").split()
    #print(values)
    for key in key_position:
      per_test_values[key].append(values[key_position[key]])
  #print(per_test_values)
  print("ITS ALL WRONG")
  assert(False)
  return per_test_values
"""


def filter_accepted_trees(iqtree_tests_file, ml_trees_file):
  ml_trees = open(ml_trees_file).readlines()
  iqtree_lines = extract_tests_results(iqtree_tests_file)
  accepted_trees = []
  for i in range(0, len(iqtree_lines)):
    line = iqtree_lines[i]
    plus_count = line.count(" + ")
    minus_count = line.count(" - ")
    assert(plus_count + minus_count == 7)
    if (minus_count == 0):
      accepted_trees.append(ml_trees[i])
  return accepted_trees

def perform_all_tests(paths):  
  iqtree_dir = os.path.join(paths.runs_dir, "iqtree_tests")
  util.mkdirp(iqtree_dir)
  iqtree_ll = iqtree_tests(paths.alignment, common.subst_model, paths.raxml_all_ml_trees, paths.raxml_best_tree, iqtree_dir)
  raxml_ll = float(open(paths.raxml_all_ml_trees_ll).readline().split(" ")[0])
  iqtree_tests_output = os.path.join(iqtree_dir, "iqtree_tests.iqtree")
  shutil.copy(iqtree_tests_output, paths.iqtree_tests_output)
  accepted_trees = filter_accepted_trees(paths.iqtree_tests_output, paths.raxml_all_ml_trees)
  print(str(len(accepted_trees)) + " tree passed all IQTree consistency tests") 
  with open(paths.raxml_credible_ml_trees, "w") as writer:
    for tree in accepted_trees:
      writer.write(tree)
  with open(paths.raxml_iqtree_ll, "w") as writer:
    writer.write("# this file contains the likelihood of the best tree at the end of the raxml-ng run, and an evaluation of likelihood of the same tree  with iqtree (with model optimization)\n")
    writer.write("raxml_ll=" + str(raxml_ll) + "\n")
    writer.write("iqtree_ll=" + str(iqtree_ll) + "\n")


