#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import placement
import convert
import util
import raxml_launcher

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
if paths.dataset_has_outgroups:
  ref_msa, query_msa = placement.split_alignment_outgroups( paths.alignment, common.outgroup_spec, epa_out_dir )
else:
  ref_msa = paths.alignment

  # create outgroup alignment using hmmer
  util.make_path_clean( hmmer_out_dir )

  #create the hmm profile
  hmm_profile = placement.launch_hmmbuild( ref_msa, hmmer_out_dir )
  # align outgroups against it
  both_phylip = placement.launch_hmmalign( hmm_profile, ref_msa, paths.outgroups_unaligned, hmmer_out_dir )
  # query_msa = os.path.join(epa_out_dir, "query.fasta")
  # convert.convert("interleaved_phylip", "fasta", query_phylip, query_msa)

  # then split for epa
  ref_msa, query_msa = placement.launch_split4epa( ref_msa, both_phylip, epa_out_dir )

# ================================================================
# then, for every tree in the credible set, do the placement
# ================================================================
result_files=[]
with open( paths.raxml_credible_ml_trees ) as ml_trees_file:
  ml_trees = ml_trees_file.readlines()
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

    # reestimate model params for the given tree
    cur_modelfile = raxml_launcher.evaluate(tree_file, ref_msa, cur_outdir)

    # place outgroup
    placement.launch_epa( tree_file, cur_modelfile, ref_msa, query_msa, cur_outdir, thorough=True )

    result_files.append( os.path.join( cur_outdir, "epa_result.jplace") )


# ================================================================
# finally, export the results
# ================================================================
result_dir = paths.epa_rooting_dir
# the overall result evaluation
placement.outgroup_check( result_files, result_dir )
# also export the individual results
for f in result_files:
  d = os.path.dirname( f )
  util.copy_dir( d, result_dir )