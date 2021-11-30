#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'scripts')
import common
import support_tree_thinning
import clade_compression_thinning
import max_entropy_thinning
import random_alignment_thinning
import util

paths = common.Paths( sys.argv )

input_tree = paths.raxml_consensus_MRE_tree 
util.mkdirp(paths.thinning_dir)

#print(ss_mre_taxa_number)


# support selection method
ss_mre_taxa_number = support_tree_thinning.support_selection_tree_thinning(input_tree, paths.ss_mre_thinned_tree)


# maximum entroy method
max_entropy_thinning.max_entropy_thinning(paths, paths.alignment, ss_mre_taxa_number, paths.me_thinned_alignment)


#clade_compression_thinning.clade_compression_thinning(paths, paths.raxml_best_tree, paths.alignment, ss_mre_taxa_number, paths.cc_thinned_alignment)
#random_alignment_thinning.thin(paths.alignment, paths.rand_thinned_alignment, ss_mre_taxa_number)


