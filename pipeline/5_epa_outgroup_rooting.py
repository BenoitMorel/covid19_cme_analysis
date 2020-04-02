#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import epa_launcher
import util

version = util.get_version( sys.argv )

tree = util.versioned_path( version, common.raxml_best_tree )
modelfile = util.versioned_path( version, common.raxml_best_model )
ref_msa = util.versioned_path( version, common.alignment )
query_msa = util.versioned_path( version, common.outgroup_alignment )
output = util.versioned_path( version, common.epa_rooting_dir )

epa_launcher.launch_epa(tree, modelfile, ref_msa, query_msa, out_dir, thorough=True)
