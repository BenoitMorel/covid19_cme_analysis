#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'scripts')
import common
import extract_dataset_from_tree

paths = common.Paths( sys.argv )

# Support Selection MRE thinned 
suffix = "-ss_mre_thinned"
tree = paths.ss_mre_thinned_tree
extract_dataset_from_tree.extract(paths, suffix, tree)

