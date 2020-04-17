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

def rec_bs_sum_thin(node, max_children, do_prune):
  if (node.is_leaf()):
    return 100
  children_tuples = []
  for child in node.get_children():
    support_sum = rec_bs_sum_thin(child, 2, do_prune)
    children_tuples.append((support_sum, child))
  # sort children by support_sum
  children_tuples.sort(key=lambda x: x[0], reverse = True)
  mysupport_sum = node.support
  for i in range(0, len(children_tuples)):
    if (i <= max_children):
      # add the support_sums of the children we keep
      mysupport_sum += children_tuples[i][0]
    else:
      # node to remove
      if (do_prune):
        node.remove_child(children_tuples[i][1])
  return mysupport_sum
"""
  Alexis' algorithm: 
"""
def max_bootstrap_sum_thinning(input_tree_file, output_tree_file):
  tree = Tree(input_tree_file, format = 0)
  print("  Initial tree size: " + str(len(tree.get_leaves())))
  tree.set_outgroup(tree.get_midpoint_outgroup())
  max_support_sum = rec_bs_sum_thin(tree, len(tree.get_children()), False) # unrooted tree -> allow 3 children
  max_tree = tree
  descendants = tree.get_descendants()
  # here comes a terrible hack based on copies
  # to iterate over all possible roots, because I
  # did not find any better way  of doing it with
  # ete3. If this becomes a serious thing, we should
  # reimplement with a better library (genesis?)
  for i in range(0, len(descendants)):
    # a leaf is never the best choice
    if (descendants[i].is_leaf()):
      continue
    copy = tree.copy()
    copy.set_outgroup(copy.get_descendants()[i])
    support_sum = rec_bs_sum_thin(copy, len(copy.get_children()), False) 
    if (max_support_sum < support_sum): 
      max_tree = copy
      max_support_sum = support_sum
  max_support_sum = rec_bs_sum_thin(max_tree, len(max_tree.get_children()), True)
  max_tree.unroot() 
  print("  Final tree size: " + str(len(max_tree.get_leaves())))
  print("    with score " + str(max_support_sum))
  with open(output_tree_file, "w") as writer:
    writer.write(max_tree.write())
  
if (__name__ == "__main__"):
  if (len(sys.argv) != 3): 
    print("Syntax: python " + os.path.basename(__file__) + " input_tree_file output_tree_file") 
    exit(1)
  input_tree_file = sys.argv[1]
  output_tree_file = sys.argv[2]
  max_bootstrap_sum_thinning(input_tree_file, output_tree_file)

