#!/usr/bin/env python

import os
import util

scripts_dir = os.path.dirname( os.path.realpath(__file__) )
base_dir = os.path.abspath( os.path.realpath( os.path.join(
            os.path.dirname( os.path.abspath( os.path.realpath( __file__ ))),
            "..")))
work_dir = os.path.join(base_dir, "work_dir")

# tools
software_path = os.path.join(base_dir, "software")
raxml = os.path.join(software_path, "raxml-ng", "bin", "raxml-ng-mpi")
old_raxml = os.path.join(software_path, "standard-RAxML", "raxml")
modeltest = os.path.join(software_path, "modeltest", "bin", "modeltest-ng-mpi")
pargenes = os.path.join(software_path, "ParGenes", "pargenes", "pargenes-hpc.py")
mptp = os.path.join(software_path, "mptp", "bin", "mptp")
epa = os.path.join(software_path, "epa-ng", "bin", "epa-ng")
papara = os.path.join(software_path, "papara", "papara")
root_digger = os.path.join(software_path, "root_digger", "bin", "rd")
genesis = os.path.join(software_path, "genesis", "bin", "apps")
genesis_reduce_duplicates = os.path.join(genesis, "reduce_duplicates")
genesis_reattach_duplicates = os.path.join(genesis, "reattach_duplicates")
genesis_convert = os.path.join(genesis, "convert")
iqtree = os.path.join(software_path, "iqtree", "bin", "iqtree")

# config
config_dir = os.path.join(base_dir, "config")
outgroup_spec = os.path.join(config_dir, "outgroups.txt")

# paths that depend on the specified version
class Paths():
  """docstring for Paths"""
  def __init__( self, argv, i=1 ):
    version = util.get_version( argv, i )

    self.version = version
    self.root_data_dir = util.versioned_path(version, self.root_data_dir)
    self.data_path = util.versioned_path(version, self.data_path)
    self.raw_alignment = util.versioned_path(version, self.raw_alignment)
    self.alignment = util.versioned_path(version, self.alignment)
    self.outgroup_alignment = util.versioned_path(version, self.outgroup_alignment)
    self.outgroups_unaligned = util.versioned_path(version, self.outgroups_unaligned)
    self.duplicates_json = util.versioned_path(version, self.duplicates_json)

    self.root_runs_dir = util.versioned_path(version, self.root_runs_dir)
    self.runs_dir = util.versioned_path(version, self.runs_dir)
    self.raxml_ml_runs_dir = util.versioned_path(version, self.raxml_ml_runs_dir)
    self.pargenes_runs_dir = util.versioned_path(version, self.pargenes_runs_dir)
    self.modeltest_runs_dir = util.versioned_path(version, self.modeltest_runs_dir)
    self.root_digger_runs_dir = util.versioned_path(version, self.root_digger_runs_dir)
    self.papara_runs_dir = util.versioned_path(version, self.papara_runs_dir)

    self.root_results_dir = util.versioned_path(version, self.root_results_dir)
    self.results_dir = util.versioned_path(version, self.results_dir)
    self.raxml_best_tree = util.versioned_path(version, self.raxml_best_tree)
    self.raxml_best_tree_tbe = util.versioned_path(version, self.raxml_best_tree_tbe)
    self.raxml_best_tree_with_duplicate = util.versioned_path(version, self.raxml_best_tree_with_duplicate)
    self.raxml_best_model = util.versioned_path(version, self.raxml_best_model)
    self.raxml_all_ml_trees = util.versioned_path(version, self.raxml_all_ml_trees)
    self.raxml_credible_ml_trees = util.versioned_path(version, self.raxml_credible_ml_trees)
    self.raxml_consensus_MR_tree = util.versioned_path(version, self.raxml_consensus_MR_tree)
    self.raxml_all_ml_trees_rf_distances = util.versioned_path(version, self.raxml_all_ml_trees_rf_distances)
    self.raxml_all_ml_trees_rf_logs = util.versioned_path(version, self.raxml_all_ml_trees_rf_logs)
    self.raxml_all_ml_trees_ll = util.versioned_path(version, self.raxml_all_ml_trees_ll)
    self.raxml_bootstrap_trees = util.versioned_path(version, self.raxml_bootstrap_trees)
    self.rf_distance_report = util.versioned_path(version, self.rf_distance_report)
    self.mptp_output = util.versioned_path(version, self.mptp_output)
    self.epa_rooting_dir = util.versioned_path(version, self.epa_rooting_dir)
    self.root_digger_output = util.versioned_path(version, self.root_digger_output)
    self.root_digger_logfile = util.versioned_path(version, self.root_digger_logfile)
    self.raxml_iqtree_ll = util.versioned_path(version, self.raxml_iqtree_ll)
    self.raxml_iqtree_ll_all = util.versioned_path(version, self.raxml_iqtree_ll_all)
    self.gamma_ll_all = util.versioned_path(version, self.gamma_ll_all)
    self.raxmlng_param_jiggle_llhs = util.versioned_path(version, self.raxmlng_param_jiggle_llhs)
    self.iqtree_param_jiggle_llhs = util.versioned_path(version, self.iqtree_param_jiggle_llhs)
    self.iqtree_tests_output = util.versioned_path(version, self.iqtree_tests_output)
  version = "UNDEFINED"
  # data
  root_data_dir = "data"
  data_path = os.path.join(root_data_dir)
  raw_alignment = os.path.join(data_path, "covid_raw.fasta")
  alignment = os.path.join(data_path, "covid_edited.fasta")
  outgroup_alignment = os.path.join(data_path, "covid_outgroups.fasta")
  outgroups_unaligned = os.path.join(data_path, "covid_outgroups_unaligned.fasta")
  duplicates_json = os.path.join(data_path, "covid_duplicates.json")

  # runs
  root_runs_dir = "runs"
  runs_dir = os.path.join(root_runs_dir)
  raxml_ml_runs_dir = os.path.join(runs_dir, "raxml_runs")
  pargenes_runs_dir = os.path.join(runs_dir, "pargenes_runs")
  modeltest_runs_dir = os.path.join(runs_dir, "modeltest_runs")
  root_digger_runs_dir = os.path.join(runs_dir, "root_digger_runs")
  papara_runs_dir = os.path.join(runs_dir, "papara_runs")

  # results
  root_results_dir = "results"
  results_dir = os.path.join(root_results_dir)
  raxml_best_tree = os.path.join(results_dir, "raxml_best_tree.newick")
  raxml_best_tree_tbe = os.path.join(results_dir, "raxml_best_tree_tbe.newick")
  raxml_best_tree_with_duplicate = os.path.join(results_dir, "raxml_best_tree_with_duplicate.newick")
  raxml_best_model = os.path.join(results_dir, "raxml_best_model.txt")
  raxml_all_ml_trees = os.path.join(results_dir, "raxml_all_ml_trees.newick")
  raxml_credible_ml_trees = os.path.join(results_dir, "raxml_credible_ml_trees.newick")
  raxml_consensus_MR_tree = os.path.join(results_dir, "raxml_consensus_tree_MR.newick")
  raxml_all_ml_trees_ll = os.path.join(results_dir, "raxml_all_ml_trees_with_ll.txt")
  raxml_bootstrap_trees = os.path.join(results_dir, "raxml_bs_trees.newick")

  raxml_all_ml_trees_rf_distances = os.path.join(results_dir, "raxml_all_ml_trees.rf.distances")
  raxml_all_ml_trees_rf_logs = os.path.join(results_dir, "raxml_all_ml_trees.rf.logs")
  rf_distance_report = os.path.join(results_dir, "rf_distance_report.txt")
  mptp_output = os.path.join(results_dir, "mptp_output.txt")
  epa_rooting_dir = os.path.join(results_dir, "epa_rooting")
  root_digger_output = os.path.join(results_dir, "root_digger_lwr.newick")
  root_digger_logfile = os.path.join(root_digger_runs_dir, "root_digger.log")
  raxml_iqtree_ll = os.path.join(results_dir, "raxml_iqtree_ll.txt")
  gamma_ll_all = os.path.join(results_dir, "gamma_ll_all.csv")
  raxml_iqtree_ll_all = os.path.join(results_dir, "raxml_iqtree_ll_all.csv")
  raxmlng_param_jiggle_llhs = os.path.join(results_dir, "raxmlng_param_jiggle_llhs.csv")
  iqtree_param_jiggle_llhs = os.path.join(results_dir, "iqtree_param_jiggle_llhs.csv")
  iqtree_tests_output = os.path.join(results_dir, "iqtree_tests.txt")
# misc
subst_model = "GTR+FO+R4"
raxml_precision = "9"
raxml_min_bl = "0.000000001"

pargenes_seed = 3000
pargenes_rand_trees = 0
pargenes_pars_trees = 100
pargenes_bs_trees = 100
pargenes_ali_name = "ali.fasta"
pargenes_family_name = pargenes_ali_name.replace(".", "_")

if (util.is_slurm()):
  available_cores = 256
else:
  available_cores = util.num_pyhsical_cores()
iqtree_threads = 4
cores_for_one_raxml_run = 4
raxmlng_eval_cores = 1
raxml_eval_cores = 1
