#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'scripts')
import common
import support_tree_thinning
import util

paths = common.Paths( sys.argv )

input_tree = paths.raxml_consensus_MRE_tree 
util.mkdirp(paths.thinning_dir)
ss_mre_taxa_number = support_tree_thinning.support_selection_tree_thinning(input_tree, paths.ss_mre_thinned_tree)

# @Lucas: ss_mre_taxa_number is the number of taxa after applying my thinning approach

