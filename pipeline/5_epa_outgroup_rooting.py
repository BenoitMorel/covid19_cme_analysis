#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import epa_launcher

paths = common.Paths( sys.argv )

tree = paths.raxml_best_tree
modelfile = paths.raxml_best_model
ref_msa = paths.alignment
query_msa = paths.outgroup_alignment
out_dir = paths.epa_rooting_dir

epa_launcher.launch_epa(tree, modelfile, ref_msa, query_msa, out_dir, thorough=True)
