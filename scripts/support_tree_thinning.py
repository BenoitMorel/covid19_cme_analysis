import sys
import os
import ete3

"""
  Class holding intermediate result for computing
  ASV (accumulated support value) score
"""
class ASVCell():
  def __init__(self):
    self.asv = 0

  


"""
  Oriented node in unrooted tree
  Follows the same scheme as pll_unode_t
  in libpll: next point to the same node but oriented to another direction, and back points to the parent of the current oriented node (back can also be seen as a child of the current node since the tree is unrooted).
  node.back.back == node
"""
class Unode():

  def __init__(self):
    self.next = self
    self.back = None
    self.support = 0.0
    self.label = None
    self.cell = None

  def is_leaf(self):
    return self.next == self

  def get_children(self, unrooted = False):
    if (self.is_leaf()):
      return None
    res = []
    it = self.next
    while (it != self):
      res.append(it.back)
      it = it.next
    if (unrooted):
      res.append(self.back)
    return res

  def get_best_asv_children(self, max_children_number, unrooted = False):
    children = self.get_children(unrooted)
    assert(len(children) >= max_children_number)
    children.sort(key=lambda x: x.cell.asv, reverse=True)
    return children[:max_children_number]

  def get_asv_as_virtual_root(self):
    # now we need 3 children, because the (virtual) root is
    # the only node with 3 children in a bifurcating tree    
    best_children = self.get_best_asv_children(3, unrooted = True)
    asv = 0
    for child in best_children:
      asv += child.cell.asv
    return asv

  def __str__(self):
    if (self.is_leaf()):
      return str(self.label)
    children = self.get_children()
    children_str = []
    for child in children:
      children_str.append(str(child))
    return "(" + ",".join(children_str) + ")" + str(self.support)

  def rec_compute_asv(self):
    if (self.cell != None): 
      # we already computed it (dynamic programming)
      return
    self.cell = ASVCell()
    if (self.is_leaf()):
      self.cell.asv = 0
      return
    children = self.get_children() 
    for child in children:
      child.rec_compute_asv()
    best_children = self.get_best_asv_children(2)
    self.cell.asv = best_children[0].cell.asv + best_children[1].cell.asv + self.support


class Utree():
  def __init__(self, newick):
    etree = ete3.Tree(newick, format = 0)
    etree.unroot()
    self.all_nodes = []
    print("Number of leaves in the ete3 tree: " + str(len(etree)))
    n = self.rec_build(etree, True)
    assert(n == None)

  def rec_build(self, enode, root = False):
    echildren = enode.get_children()
    if (len(echildren) == 0):
      leaf = Unode()
      self.all_nodes.append(leaf)
      leaf.next = leaf
      leaf.label = enode.name
      return leaf
    children = [] 
    node = None
    if (not root):
      node = Unode()
      self.all_nodes.append(node)
      children.append(node)
    for echild in echildren:
      child = Unode()
      self.all_nodes.append(child)
      child.back = self.rec_build(echild)
      child.back.back = child
      support = echild.support
      if (echild.is_leaf()):
        support = 0
      child.support = support
      child.back.support = support
      children.append(child)
      if (len(children) > 1):
        children[-2].next = children[-1]
    assert(len(children) > 2)
    children[-1].next = children[0]
    return node

  def get_any_internal_node(self):
    res = self.all_nodes[len(self.all_nodes) / 2]
    #res = self.all_nodes[0]
    if (res.is_leaf()):
      res = res.back
    return res

  def __str__(self):
    n = self.get_any_internal_node()
    children = n.get_children(unrooted = True)
    children_str = []
    for child in children:
      children_str.append(str(child))
    return "(" + ",".join(children_str) + ");"
  
  def compute_asv(self):
    for node in self.all_nodes:
      node.rec_compute_asv()

  def get_best_virtual_root(self):
    best_asv = 0
    best_node = None
    for node in self.all_nodes:
      if (node.is_leaf()):
        continue
      asv = node.get_asv_as_virtual_root()
      if (asv > best_asv):
        best_asv = asv
        best_node = node
    
    print("Best asv: " + str(best_asv))
    return best_node

  def get_best_asv_newick_rec(self, node):
    if (node.is_leaf()):
      return node.label
    best_children = node.get_best_asv_children(2)
    newicks = []
    for child in best_children:
      newicks.append(self.get_best_asv_newick_rec(child))
    return "(" + ",".join(newicks) + ")"

  """
    Main function for asv pruning. Calls all the other
    helper functions
  """
  def compute_best_asv_newick(self):
    self.compute_asv()
    best_root = self.get_best_virtual_root()
    best_children = best_root.get_best_asv_children(3, unrooted = True)
    newicks = []
    for child in best_children:
      newicks.append(self.get_best_asv_newick_rec(child))
    return "(" + ",".join(newicks) + ");"



def support_selection_tree_thinning(input_tree_filename, output_tree_filename):
  tree = Utree(input_tree_filename)
  pruned_newick = tree.compute_best_asv_newick()
  tree = Utree(pruned_newick)
  open(output_tree_filename, "w").write(pruned_newick)
  return len(ete3.Tree(output_tree_filename).get_leaves())

"""
  One single test is better than no test at all
"""
def unit_test():
  tree_str1 = "((a,b)50,(c,d)50,(e,f)49,(x,y)0)25"
  tree_str2 = "((g,h)25,(i,j)25,(k,(l,m)80)24)25"
  tree_str3 = "((o,p)10,(q,r)10)15"
  tree_str = "(" + tree_str1 + "," + tree_str2 + "," + tree_str3 + ")100;"
  print("Ete3 tree:")
  etree = ete3.Tree(tree_str, format = 1)
  etree.unroot()
  print(etree)
  tree = Utree(tree_str) 
  print("Utree: ")
  print(tree)
  pruned_newick = tree.compute_best_asv_newick()
  print("Pruned newick: ")
  print(pruned_newick)
  final_etree = ete3.Tree(pruned_newick, format = 1)
  print("Pruned ete3 tree: ")
  print(final_etree)
  print("Number of leaves in the final tree: " + str(len(final_etree)))
  assert(tree.get_best_virtual_root().get_asv_as_virtual_root() == 314.0)

if (__name__ == "__main__"):
  if (len(sys.argv) == 1):
    print("running unit test")
    unit_test()
    sys.exit(0)
  if (len(sys.argv) != 3): 
    print("Syntax: python " + os.path.basename(__file__) + " input_tree_file output_tree_file") 
    exit(1)
  input_tree_file = sys.argv[1]
  output_tree_file = sys.argv[2]
  support_selection_tree_thinning(input_tree_file, output_tree_file)


