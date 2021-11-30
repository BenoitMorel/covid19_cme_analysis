#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'scripts')
import common
import thinned_dataset_extraction

paths = common.Paths( sys.argv )

# Support Selection thinning 
thinned_dataset_extraction.extract_ss(paths, "-ss_thinned", paths.ss_mre_thinned_tree)

# Max entropy thinning
thinned_dataset_extraction.extract_me(paths, "-me_thinned", paths.me_thinned_alignment)

# Clade compression thinning
#thinned_dataset_extraction.extract_cc(paths, "-cc_thinned", paths.cc_thinned_alignment)

# Random thinning
#thinned_dataset_extraction.extract_rand(paths, "-rand_thinned", paths.rand_thinned_alignment)


