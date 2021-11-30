import common
import util
import data_versioning
import shutil
from ete3 import Tree
from ete3 import SeqGroup


def extract_ss(input_path, suffix, tree_file): 
  print("Extracting alignment generated with the support selection tree thinning technique...")
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
  open(output_path.alignment, "w").write(new_msa.write(format = "fasta"))
  shutil.copy(input_path.duplicates_json, output_path.duplicates_json)
  shutil.copy(input_path.outgroups_file, output_path.outgroups_file)
  print("New version of the snapshot: " + output_path.path)

def extract_me(input_path, suffix, alignment_file):
  print("Extracting alignment generated with the maximum entropy tree thinning technique...")
  path_argv = [input_path._version, input_path._dataset + suffix]
  output_path = common.Paths(path_argv, 0)
  data_versioning.setup_new_dataset(output_path)
  shutil.copy(alignment_file, output_path.alignment)
  shutil.copy(input_path.outgroups_file, output_path.outgroups_file)
  shutil.copy(input_path.duplicates_json, output_path.duplicates_json)
  print("New version of the snapshot: " + output_path.path)

def extract_cc(input_path, suffix, alignment_file):
  path_argv = [input_path._version, input_path._dataset + suffix]
  output_path = common.Paths(path_argv, 0)
  data_versioning.setup_new_dataset(output_path)
  shutil.copy(alignment_file, output_path.alignment)
  shutil.copy(input_path.outgroups_file, output_path.outgroups_file)
  shutil.copy(input_path.duplicates_json, output_path.duplicates_json)
  print("New version of the snapshot: " + output_path.path)

def extract_rand(input_path, suffix, alignment_file):
  path_argv = [input_path._version, input_path._dataset + suffix]
  output_path = common.Paths(path_argv, 0)
  data_versioning.setup_new_dataset(output_path)
  shutil.copy(alignment_file, output_path.alignment)
  shutil.copy(input_path.outgroups_file, output_path.outgroups_file)
  shutil.copy(input_path.duplicates_json, output_path.duplicates_json)
  print("New version of the snapshot: " + output_path.path)


