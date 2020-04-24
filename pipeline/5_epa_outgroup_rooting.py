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
hmmer_out_dir = paths.hmmer_runs_dir

# create outgroup alignment using papara
util.clean_dir( hmmer_out_dir )
util.make_path( hmmer_out_dir )

#create the hmm profile
hmm_profile = epa_launcher.launch_hmmbuild( ref_msa, hmmer_out_dir )
# align outgroups against it
both_phylip = epa_launcher.launch_hmmalign( hmm_profile, paths.outgroups_unaligned, hmmer_out_dir )
# convert.convert( "phylip", "fasta", both_phylip, query_msa )

# then split for epa
ref_msa, query_msa = epa_launcher.launch_split4epa( ref_msa_phylip, both_phylip, hmmer_out_dir )

# place outgroup
epa_launcher.launch_epa( tree, modelfile, ref_msa, query_msa, epa_out_dir, thorough=True )
