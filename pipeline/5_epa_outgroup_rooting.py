#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import epa_launcher
import convert
import util

paths = common.Paths( sys.argv )

tree = paths.raxml_best_tree
modelfile = paths.raxml_best_model
ref_msa = paths.alignment
query_msa = paths.outgroup_alignment
epa_out_dir = paths.epa_rooting_dir
papara_out_dir = paths.papara_runs_dir

# create outgroup alignment using papara
# first create a phylip version of the ref alignment
util.clean_dir( papara_out_dir )
util.make_path( papara_out_dir )
ref_msa_phylip = os.path.join( papara_out_dir, "covid_ingroup.phylip" )
convert.convert( "fasta", "phylip", ref_msa, ref_msa_phylip )
# then align
papara_result = epa_launcher.launch_papara( tree, ref_msa_phylip, paths.outgroups_unaligned, papara_out_dir )
# then split for epa
ref_msa, query_msa = epa_launcher.launch_split4epa( ref_msa_phylip, papara_result, papara_out_dir )

# place outgroup
epa_launcher.launch_epa( tree, modelfile, ref_msa, query_msa, epa_out_dir, thorough=True )
