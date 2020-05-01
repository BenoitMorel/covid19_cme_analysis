#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import epa_launcher
import convert
import util

paths = common.Paths( sys.argv )

# tree = paths.raxml_best_tree
modelfile = paths.raxml_best_model
epa_out_dir = paths.epa_runs_dir
hmmer_out_dir = paths.hmmer_runs_dir

try:
  util.expect_file_exists( paths.raxml_credible_ml_trees )
except Exception as e:
  print("ERROR: Must run iqtree_tests stage of pipeline first")
  raise e

# ================================================================
# start by ensuring we have the outgroups aligned against the ref
# ================================================================

# if outgroup is included in the alignment, separate the two from the alignment currently seen as final
if paths.msa_has_outgroups():
  ref_msa, query_msa = epa_launcher.split_alignment_outgroups( paths.alignment, common.outgroup_spec, epa_out_dir )
else:
  # create outgroup alignment using hmmer
  util.make_path_clean( hmmer_out_dir )

  #create the hmm profile
  hmm_profile = epa_launcher.launch_hmmbuild( ref_msa, hmmer_out_dir )
  # align outgroups against it
  both_phylip = epa_launcher.launch_hmmalign( hmm_profile, paths.outgroups_unaligned, hmmer_out_dir )

  # then split for epa
  ref_msa, query_msa = epa_launcher.launch_split4epa( ref_msa_phylip, both_phylip, epa_out_dir )

# ================================================================
# then, for every tree in the credible set, do the placement
# ================================================================
result_files=[]
with open( paths.raxml_credible_ml_trees ).readlines() as ml_trees:
  i = 0
  for tree in ml_trees:
    # subdirs per tree
    cur_outdir = os.path.join( epa_out_dir, str(i) )
    i += 1
    util.make_path_clean( cur_outdir )

    # write down the tree into a file for epa to use
    tree_file = os.path.join( cur_outdir, "tree.newick" )
    with open(tree_file, 'w') as f:
      print( tree, file=f )

    # place outgroup
    epa_launcher.launch_epa( tree_file, modelfile, ref_msa, query_msa, cur_outdir, thorough=True )

    result_files.append( os.path.join( cur_outdir, "epa_result.jplace") )


# ================================================================
# finally, export the results
# ================================================================
result_dir = paths.epa_rooting_dir
# TODO

