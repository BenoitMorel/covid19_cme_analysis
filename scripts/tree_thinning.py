import sys
import os
from ete3 import Tree

def rec_leaves_thinning(node, leaves_to_keep):
  if (node.is_leaf()):
    return
  leaf_children = 0
  for child in node.get_children():
    if (child.is_leaf()):
      leaf_children += 1
      if (leaf_children <= 2):
        leaves_to_keep.append(child)
    else:
      rec_leaves_thinning(child, leaves_to_keep)
"""
  For each node n, remove children until there are at most 
  2 leaves under n
"""
def leaves_thinning(input_tree_file, output_tree_file):
  tree = Tree(input_tree_file, format = 1)
  assert(len(tree.get_children()) == 3)
  print("Taxa number: " + str(len(tree.get_leaves())))
  leaves_to_keep = []
  rec_leaves_thinning(tree, leaves_to_keep)
  tree.prune(leaves_to_keep)
  print("leaves to keep size: " + str(len(leaves_to_keep)))
  assert(len(leaves_to_keep) == len(tree.get_leaves()))
  with open(output_tree_file, "w") as writer:
    writer.write(tree.write())


if (__name__ == "__main__"):
  if (len(sys.argv) != 3): 
    print("Syntax: python " + os.path.basename(__file__) + " input_tree_file output_tree_file") 
    exit(1)
  input_tree_file = sys.argv[1]
  output_tree_file = sys.argv[2]
  leaves_thinning(input_tree_file, output_tree_file)

