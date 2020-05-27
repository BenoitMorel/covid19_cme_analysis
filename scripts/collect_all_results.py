import sys
import os
from common import Paths
import common
import data_versioning
import util
import ete3

def get_taxa_number(path):
  tree = ete3.Tree(path.raxml_best_tree, format = 1)
  return len(tree.get_leaves())

def credible_trees_num(path):
  return len(open(path.raxml_credible_ml_trees).readlines())

def get_resolution_ratio(tree_path):
  tree = ete3.Tree(tree_path, format = 1)
  leaves_number = len(tree.get_leaves())
  bifurcations_number = 0
  for node in tree.traverse("postorder"):
    if (node.is_root()):
      if (len(node.get_children()) <= 3):
        bifurcations_number += 1
    else:
      if (len(node.get_children()) == 2):
        bifurcations_number += 1
  return float(bifurcations_number) / float(leaves_number - 2)

def str3(v):
  return str(round(v, 3))

def get_ml_trees_rf(path):
  line = open(path.rf_distance_report).readlines()[0]
  assert("Average pairwise RF distance between all ML trees" in line)
  return float(line.replace("\n", "").split()[-1])

def get_search_rf(path):
  line = open(path.rf_distance_report).readlines()[2]
  assert("RF distance between start and ML trees" in line)
  return float(line.replace("\n", "").split()[-1])



def print_report(version, dataset):
  path = Paths.from_version_and_dataset(version, dataset)
  mr_res_ratio = get_resolution_ratio(path.raxml_consensus_MR_tree)
  mre_res_ratio = get_resolution_ratio(path.raxml_consensus_MRE_tree)
  print(dataset + ":")
  print("\tTaxa number: " + str(get_taxa_number(path)))
  print("\tRFD(ML trees): " + str3(get_ml_trees_rf(path)))
  print("\tRFD(parsimony, ML): " + str3(get_search_rf(path)))
  print("\tCredible trees: " + str(credible_trees_num(path)))
  print("\tMR tree resolution ratio: " + str3(mr_res_ratio))
  print("\tMRE tree resolution ratio: " + str3(mre_res_ratio))
  
  print("")


if __name__ == '__main__':
  if (len(sys.argv) != 2):
    print("Syntax python " + os.path.basename(__file__) + " version")
    sys.exit(1)
  version = sys.argv[1]
 

  for dataset in Paths.get_all_datasets(version):
    print_report(version, dataset)


