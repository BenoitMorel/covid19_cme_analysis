#!/usr/bin/env python
import os
import sys
sys.path.insert(0, 'scripts')
import common
import iqtree_tests
import build_consensus_tree
paths = common.Paths( sys.argv )

iqtree_tests.perform_all_tests(paths)

credible_trees = paths.raxml_credible_ml_trees
output_tree = paths.raxml_consensus_MR_tree
run_dir = os.path.join(paths.runs_dir, "consensus")
mode = "MR"
build_consensus_tree.build_consensus_tree(credible_trees, output_tree, run_dir, mode)



