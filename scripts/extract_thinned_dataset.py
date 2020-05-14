import common
import util
import data_versioning
import shutil
from ete3 import Tree
from ete3 import SeqGroup


def extract(input_path, suffix, tree_file): 
  
  tree = Tree(tree_file, format = 1)
  leaves_set = set(tree.get_leaf_names())
  msa = SeqGroup(input_path.alignment, "fasta")
  path_argv = [input_path._version, input_path._dataset + suffix]
  output_path = common.Paths(path_argv, 0)
  data_versioning.setup_new_dataset(output_path)
  new_msa = SeqGroup()
  for entry in msa.iter_entries():
    label = entry[0]
    sequence = entry[1]
    if (label in leaves_set):
      new_msa.set_seq(label, sequence)
  print("Saving alignment with " + str(len(new_msa)) + " sequences in " + output_path.alignment)
  open(output_path.alignment, "w").write(new_msa.write(format = "fasta"))
  shutil.copy(input_path.duplicates_json, output_path.duplicates_json)

