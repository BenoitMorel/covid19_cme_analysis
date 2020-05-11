#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'scripts')
import common
import support_tree_thinning
import util

paths = common.Paths( sys.argv )

input_tree = paths.raxml_consensus_MR_tree 
util.mkdirp(paths.thinning_dir)
support_tree_thinning.support_selection_tree_thinning(input_tree, paths.max_support_thinned_tree)

