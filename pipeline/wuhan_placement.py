#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import placement
import convert
import util

paths = common.Paths( sys.argv )

# lay some stones in the wrong path
try:
  util.expect_dir_exists( paths.epa_rooting_dir )
except Exception as e:
  print("ERROR: Must run placement stage of pipeline first")
  raise e

# get a separate workdir for this task
runs_dir = paths.wuhan_placement_runs_dir
# also a separate results dir
result_dir = paths.wuhan_placement_dir

util.make_path_clean( runs_dir )
util.make_path_clean( result_dir )

# get the wuhan sequence out of the master raw file into its own file in
# the runs dir
wuhan_fasta = os.path.join( runs_dir, "sequence.fasta" )

placement.extract_sequence( paths.raw_sequences, "EPI_ISL_406801", wuhan_fasta )

ref_msa = paths.alignment

# check if there already is a hmmprofile (should be the case for *msan runs)
hmm_profile = os.path.join( paths.hmmer_runs_dir, "reference.hmm" )
# build it if it doesn't exist
if not os.path.isfile( hmm_profile ):
  hmm_profile = placement.launch_hmmbuild( ref_msa, paths.hmmer_runs_dir )

# align the wuhan sequence against the master MSA
both_msa = placement.launch_hmmalign( hmm_profile, ref_msa, wuhan_fasta, runs_dir )
ref_msa, query_msa = placement.launch_split4epa( ref_msa, both_msa, runs_dir )

# ================================================================
# for every tree in the credible set, do the placement
# ================================================================
result_files=[]
with open( paths.raxml_credible_ml_trees ) as ml_trees_file:
  ml_trees = ml_trees_file.readlines()
  total = len(ml_trees) - 1
  i = 0
  for tree in ml_trees:
    print(i, " / ", total)
    # subdirs per tree
    cur_outdir = os.path.join( runs_dir, str(i) )
    epa_result_subdir = os.path.join( paths.epa_rooting_dir, str(i) )
    expect_dir_exists( epa_result_subdir )
    i += 1
    util.make_path_clean( cur_outdir )

    # get the same treefile as used in the normal epa runs
    tree_file = os.path.join( epa_result_subdir, "tree.newick" )
    util.expect_file_exists( tree_file )

    # fetch the previously created model file
    cur_modelfile = epa_result_subdir + "eval.raxml.bestModel"
    util.expect_file_exists( cur_modelfile )

    # place the wuhan seq
    placement.launch_epa( tree_file, cur_modelfile, ref_msa, query_msa, cur_outdir, thorough=True )

    result_files.append( os.path.join( cur_outdir, "epa_result.jplace") )

# ================================================================
# post-analysis
# ================================================================
# do the summary high level stats
placement.outgroup_check( result_files, result_dir )
# also generate the lwr histograms
hist_csv_file = placement.gappa_examine_lwr( os.path.join( runs_dir, "*/*.jplace" ), result_dir )
placement.ggplot_lwr_histogram( hist_csv_file, result_dir)

# ================================================================
# finally, export the results
# ================================================================
# also export the individual results
for f in result_files:
  d = os.path.dirname( f )
  util.copy_dir( d, os.path.join( result_dir, os.path.basename(d) ), ["*.rba", "*.phy", "*.startTree"] )
