#!/usr/bin/env python3

import os
import util

FNULL = open(os.devnull, 'w')

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
genesis_remove_sequences = os.path.join(genesis, "remove_sequences")
genesis_outgroup_check = os.path.join(genesis, "jplace_outgroup_check")
iqtree = os.path.join(software_path, "iqtree", "bin", "iqtree")
preanalysis1 = os.path.join(scripts_dir, "preanalysis1.sh")
mafft = os.path.join(software_path, "mafft", "mafft.bat")
hmmer_dir = os.path.join(software_path, "hmmer", "src")

# config
config_dir = os.path.join(base_dir, "config")
outgroup_spec = os.path.join(config_dir, "outgroups.txt")

# paths that depend on the specified version
class Paths():
  """docstring for Paths"""
  def __init__( self, argv, i=1 ):
    version = util.get_version( argv[:-1], i )

    self._version = version
    self._dataset = argv[-1] #dataset
    # options: ["fmsao", "fmsan", "smsao", "smsan"]

    os.makedirs(util.make_path_in_workdir(self.version, self.dataset),
        exist_ok=True)

  # =====================================================
  # FUNCTIONS and basic values
  # =====================================================

  @property
  def dataset_has_outgroups(self):
    return self._dataset[-1] == 'o'

  @property
  def dataset_had_singletons_removed(self):
    return self._dataset[0] == 's'

  @property
  def version(self):
    return self._version

  @property
  def dataset(self):
    return self._dataset

  # =====================================================
  # DATA
  # =====================================================

  @property
  def raw_sequences(self):
    return util.make_path_in_workdir(self.version, self._raw_sequences)

  @property
  def root_data_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._root_data_dir)

  @property
  def data_path(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._data_path)

  @property
  def raw_alignment(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raw_alignment)

  @property
  def alignment(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._alignment)

  @property
  def outgroups_unaligned(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._outgroups_unaligned)

  @property
  def duplicates_json(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._duplicates_json)

  # =====================================================
  # RUNS
  # =====================================================

  @property
  def root_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._root_runs_dir)

  @property
  def runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._runs_dir)

  @property
  def preanalysis_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._preanalysis_runs_dir)

  @property
  def raxml_ml_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_ml_runs_dir)

  @property
  def pargenes_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._pargenes_runs_dir)

  @property
  def modeltest_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._modeltest_runs_dir)

  @property
  def root_digger_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._root_digger_runs_dir)

  @property
  def papara_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._papara_runs_dir)

  @property
  def hmmer_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._hmmer_runs_dir)

  @property
  def epa_runs_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._epa_runs_dir)

  # =====================================================
  # RESULTS
  # =====================================================

  @property
  def root_results_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._root_results_dir)

  @property
  def results_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._results_dir)

  @property
  def raxml_best_tree(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_best_tree)

  @property
  def raxml_best_tree_tbe(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_best_tree_tbe)

  @property
  def raxml_best_tree_with_duplicate(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_best_tree_with_duplicate)

  @property
  def raxml_best_model(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_best_model)

  @property
  def raxml_all_ml_trees(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_all_ml_trees)

  @property
  def raxml_credible_ml_trees(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_credible_ml_trees)

  @property
  def raxml_consensus_MR_tree(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_consensus_MR_tree)

  @property
  def raxml_all_ml_trees_rf_distances(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_all_ml_trees_rf_distances)

  @property
  def raxml_all_ml_trees_rf_logs(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_all_ml_trees_rf_logs)

  @property
  def raxml_all_ml_trees_ll(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_all_ml_trees_ll)

  @property
  def raxml_bootstrap_trees(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_bootstrap_trees)

  @property
  def rf_distance_report(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._rf_distance_report)

  @property
  def mptp_output(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._mptp_output)

  @property
  def thinning_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._thinning_dir)

  @property
  def max_support_thinned_tree(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._max_support_thinned_tree)

  @property
  def leaves_thinned_tree(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._leaves_thinned_tree)

  @property
  def epa_rooting_dir(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._epa_rooting_dir)

  @property
  def root_digger_output(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._root_digger_output)

  @property
  def root_digger_logfile(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._root_digger_logfile)

  @property
  def raxml_iqtree_ll(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_iqtree_ll)

  @property
  def raxml_iqtree_ll_all(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxml_iqtree_ll_all)

  @property
  def gamma_ll_all(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._gamma_ll_all)

  @property
  def gamma_median_ll_all(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._gamma_median_ll_all)

  @property
  def raxmlng_param_jiggle_llhs(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._raxmlng_param_jiggle_llhs)

  @property
  def iqtree_param_jiggle_llhs(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._iqtree_param_jiggle_llhs)

  @property
  def iqtree_tests_output(self):
    return util.make_path_in_workdir(self.version, self.dataset, self._iqtree_tests_output)

  _version = "UNDEFINED"

  # dl from gisaid
  _raw_sequences = "covid_raw_unaligned.fasta"

  # data
  _root_data_dir = "data"
  _data_path = os.path.join(_root_data_dir)
  _raw_alignment = os.path.join(_data_path, "covid_raw.fasta")
  _alignment = os.path.join(_data_path, "covid_edited.fasta")
  _duplicates_json = os.path.join(_data_path, "covid_duplicates.json")

  # runs
  _root_runs_dir = "runs"
  _runs_dir = os.path.join(_root_runs_dir)
  _preanalysis_runs_dir = os.path.join(_runs_dir, "preanalysis_runs")
  _raxml_ml_runs_dir = os.path.join(_runs_dir, "raxml_runs")
  _pargenes_runs_dir = os.path.join(_runs_dir, "pargenes_runs")
  _modeltest_runs_dir = os.path.join(_runs_dir, "modeltest_runs")
  _root_digger_runs_dir = os.path.join(_runs_dir, "root_digger_runs")
  _papara_runs_dir = os.path.join(_runs_dir, "papara_runs")
  _hmmer_runs_dir = os.path.join(_runs_dir, "hmmer_runs")
  _epa_runs_dir = os.path.join(_runs_dir, "epa_runs")


  # results
  _root_results_dir = "results"
  _results_dir = os.path.join(_root_results_dir)
  _raxml_best_tree = os.path.join(_results_dir, "raxml_best_tree.newick")
  _raxml_best_tree_tbe = os.path.join(_results_dir, "raxml_best_tree_tbe.newick")
  _raxml_best_tree_with_duplicate = os.path.join(_results_dir, "raxml_best_tree_with_duplicate.newick")
  _raxml_best_model = os.path.join(_results_dir, "raxml_best_model.txt")
  _raxml_all_ml_trees = os.path.join(_results_dir, "raxml_all_ml_trees.newick")
  _raxml_credible_ml_trees = os.path.join(_results_dir, "raxml_credible_ml_trees.newick")
  _raxml_consensus_MR_tree = os.path.join(_results_dir, "raxml_consensus_tree_MR.newick")
  _raxml_all_ml_trees_ll = os.path.join(_results_dir, "raxml_all_ml_trees_with_ll.txt")
  _raxml_bootstrap_trees = os.path.join(_results_dir, "raxml_bs_trees.newick")

  _outgroups_unaligned = os.path.join(_preanalysis_runs_dir, "covid_outgroups.fasta")

  _raxml_all_ml_trees_rf_distances = os.path.join(_results_dir, "raxml_all_ml_trees.rf.distances")
  _raxml_all_ml_trees_rf_logs = os.path.join(_results_dir, "raxml_all_ml_trees.rf.logs")
  _rf_distance_report = os.path.join(_results_dir, "rf_distance_report.txt")
  _mptp_output = os.path.join(_results_dir, "mptp_output.txt")
  _thinning_dir = os.path.join(_results_dir, "tree_thinning")
  _max_support_thinned_tree = os.path.join(_thinning_dir, "max_support_thinned_tree.newick")
  _leaves_thinned_tree = os.path.join(_thinning_dir, "leaves_thinned_tree.newick")
  _epa_rooting_dir = os.path.join(_results_dir, "epa_rooting")
  _root_digger_output = os.path.join(_results_dir, "root_digger_lwr.newick")
  _root_digger_logfile = os.path.join(_root_digger_runs_dir, "root_digger.log")
  _raxml_iqtree_ll = os.path.join(_results_dir, "raxml_iqtree_ll.txt")
  _gamma_ll_all = os.path.join(_results_dir, "gamma_ll_all.csv")
  _gamma_median_ll_all = os.path.join(_results_dir, "gamma_median_ll_all.csv")
  _raxml_iqtree_ll_all = os.path.join(_results_dir, "raxml_iqtree_ll_all.csv")
  _raxmlng_param_jiggle_llhs = os.path.join(_results_dir, "raxmlng_param_jiggle_llhs.csv")
  _iqtree_param_jiggle_llhs = os.path.join(_results_dir, "iqtree_param_jiggle_llhs.csv")
  _iqtree_tests_output = os.path.join(_results_dir, "iqtree_tests.txt")

# misc
subst_model = "GTR+FO+G4"
raxml_precision = "9"
raxml_min_bl = "0.000000001"

pargenes_seed = 3000
pargenes_rand_trees = 0
pargenes_pars_trees = 100
pargenes_bs_trees = 0
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
