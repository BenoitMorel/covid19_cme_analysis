#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'scripts')
import common
import iqtree_tests
import build_consensus_tree
paths = common.Paths( sys.argv )

iqtree_tests.perform_all_tests(paths)

credible_trees = paths.raxml_credible_ml_trees
run_dir = os.path.join(paths.runs_dir, "consensus")

mode_to_tree = {}
mode_to_tree["MR"] = paths.raxml_consensus_MR_tree
mode_to_tree["MRE"] = paths.raxml_consensus_MRE_tree

for mode in mode_to_tree:
  build_consensus_tree.build_consensus_tree(credible_trees, mode_to_tree[mode], run_dir, mode)



