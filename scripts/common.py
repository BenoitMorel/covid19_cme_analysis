#!/usr/bin/env python3

import os
import util
import re

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
mptp_fix = os.path.join(software_path, "mptp_fix", "bin", "mptp")
epa = os.path.join(software_path, "epa-ng", "bin", "epa-ng")
papara = os.path.join(software_path, "papara", "papara")
root_digger = os.path.join(software_path, "root_digger", "bin", "rd")
genesis = os.path.join(software_path, "genesis", "bin", "apps")
genesis_reduce_duplicates = os.path.join(genesis, "reduce_duplicates")
genesis_reattach_duplicates = os.path.join(genesis, "reattach_duplicates")
genesis_convert = os.path.join(genesis, "convert")
genesis_clade_compression = os.path.join(genesis, "prune_tree_by_entropy")
genesis_max_entropy = os.path.join(genesis, "maximize_entropy")
genesis_remove_sequences = os.path.join(genesis, "remove_sequences")
genesis_outgroup_check = os.path.join(genesis, "jplace-outgroup-check")
genesis_mptp_all_rootings = os.path.join(genesis, "mptp_all_rootings")
gappa = os.path.join(software_path, "gappa", "bin", "gappa")
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
    argv = util.preprocess_argv(argv, i)
    version = util.get_version( argv[:-1], i )
    self._version = version
    self._dataset = argv[-1] #dataset
    self._version_root = util.make_path_in_workdir(self.version)
    self._dataset_root = os.path.join(self._version_root, self.dataset)

    # we need to create a Path like that
    # when extracting a thinned dataset
    util.mkdirp(self._dataset_root)
    
  #if not os.path.isdir( self._dataset_root ):
  #    util.fail( "No such dataset: " + self.dataset )

    # os.makedirs(self._dataset_root, exist_ok=True)
      # why is this here this should fail!

  def from_version_and_dataset(version, data):
    return Paths([version, data], 0)

  def get_all_datasets(version):
    version_path = util.make_path_in_workdir(version)
    datasets = []
    version_dir = util.make_path_in_workdir(version)
    for dataset in os.listdir(version_dir):
      datadir = os.path.join(version_dir, dataset)
      if (os.path.isdir(datadir)):
        if ("results" in os.listdir(datadir)):
          datasets.append(dataset)
    return sorted(datasets)

  # =====================================================
  # FUNCTIONS and basic values
  # =====================================================

  @property
  def dataset_has_outgroups(self):
    return re.search("msa.", self._dataset).group(0)[-1] == 'o'

  @property
  def dataset_had_singletons_removed(self):
    return re.search(".msa", self._dataset).group(0)[0] == 's'

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
    return os.path.join(self._version_root, "covid_raw_unaligned.fasta")

  @property
  def data_dir(self):
    return os.path.join(self._dataset_root, "data")

  @property
  def raw_alignment(self):
    return os.path.join(self.data_dir, "covid_raw.fasta")

  @property
  def alignment(self):
    return os.path.join(self.data_dir, "covid_edited.fasta")

  @property
  def outgroups_file(self):
    return os.path.join(self.data_dir, "covid_outgroups.fasta")

  @property
  def duplicates_json(self):
    return os.path.join(self.data_dir, "covid_duplicates.json")

  # =====================================================
  # RUNS
  # =====================================================

  @property
  def runs_dir(self):
    return os.path.join(self._dataset_root, "runs")

  @property
  def preanalysis_runs_dir(self):
    return os.path.join(self.runs_dir, "preanalysis_runs")

  @property
  def raxml_ml_runs_dir(self):
    return os.path.join(self.runs_dir, "raxml_runs")

  @property
  def pargenes_runs_dir(self):
    return os.path.join(self.runs_dir, "pargenes_runs")

  @property
  def modeltest_runs_dir(self):
    return os.path.join(self.runs_dir, "modeltest_runs")

  @property
  def root_digger_runs_dir(self):
    return os.path.join(self.runs_dir, "root_digger_runs")

  @property
  def papara_runs_dir(self):
    return os.path.join(self.runs_dir, "papara_runs")

  @property
  def hmmer_runs_dir(self):
    return os.path.join(self.runs_dir, "hmmer_runs")

  @property
  def epa_runs_dir(self):
    return os.path.join(self.runs_dir, "epa_runs")

  @property
  def wuhan_placement_runs_dir(self):
    return os.path.join(self.runs_dir, "wuhan_placement_runs")

  @property
  def cc_thinning_runs_dir(self):
    return os.path.join(self.runs_dir, "cc_thinning_runs")

  @property
  def me_thinning_runs_dir(self):
    return os.path.join(self.runs_dir, "me_thinning_runs")

  # =====================================================
  # RESULTS
  # =====================================================

  @property
  def results_dir(self):
    return os.path.join(self._dataset_root, "results")
  
  @property
  def trees_dir(self):
    res = os.path.join(self.results_dir, "trees")
    util.mkdirp(res)
    return res
  
  @property 
  def rfdistance_dir(self):
    res = os.path.join(self.results_dir, "rfdistances")
    util.mkdirp(res)
    return res

  @property
  def models_dir(self):
    res = os.path.join(self.results_dir, "models")
    util.mkdirp(res)
    return res

  @property
  def species_delimitation_dir(self):
    res = os.path.join(self.results_dir, "species_delimitation")
    util.mkdirp(res)
    return res

  @property
  def species_delimitation_runs_dir(self):
    res = os.path.join(self.runs_dir, "species_delimitation")
    util.mkdirp(res)
    return res

  @property 
  def likelihoods_dir(self):
    res = os.path.join(self.results_dir, "likelihoods")
    util.mkdirp(res)
    return res

  @property
  def thinning_dir(self):
    res = os.path.join(self.results_dir, "tree_thinning")
    util.mkdirp(res)
    return res
  
  @property
  def epa_rooting_dir(self):
    return os.path.join(self.results_dir, "epa_rooting")

  @property
  def wuhan_placement_dir(self):
    return os.path.join(self.results_dir, "wuhan_placement")

  @property
  def rootdigger_dir(self):
    res = os.path.join(self.results_dir, "rootdigger_rooting")
    util.mkdirp(res)
    return res

  @property
  def raxml_best_tree(self):
    return os.path.join(self.trees_dir, "best_ml_tree.newick")

  @property
  def raxml_best_tree_tbe(self):
    return os.path.join(self.trees_dir, "best_ml_tree.newick_tbe.newick")

  @property
  def raxml_bootstrap_trees(self):
    return os.path.join(self.trees_dir, "bootstrap_trees.newick")

  @property
  def raxml_best_tree_with_duplicate(self):
    return os.path.join(self.trees_dir, "best_ml_tree.newick_duplicate_reattached.newick")

  @property
  def raxml_all_ml_trees(self):
    return os.path.join(self.trees_dir, "all_ml_trees.newick")

  @property
  def raxml_credible_ml_trees(self):
    return os.path.join(self.trees_dir, "credible_ml_trees.newick")

  @property
  def raxml_consensus_MR_tree(self):
    return os.path.join(self.trees_dir, "MR_consensus_tree.newick")

  @property
  def raxml_consensus_MRE_tree(self):
    return os.path.join(self.trees_dir, "MRE_consensus_tree.newick")

  @property
  def raxml_all_ml_trees_rf_distances(self):
    return os.path.join(self.rfdistance_dir, "all_rfdistances.txt")

  @property
  def rf_distance_report(self):
    return os.path.join(self.rfdistance_dir, "summary.txt")
 

  @property
  def raxml_best_model(self):
    return os.path.join(self.models_dir, "raxml_best_model.txt")

  @property
  def mptp_output(self):
    return os.path.join(self.species_delimitation_runs_dir, "mptp_output")

  @property
  def mptp_output_csv(self):
    return os.path.join(self.species_delimitation_dir, "mptp.csv")

  @property
  def mptp_output_summary(self):
    return os.path.join(self.species_delimitation_dir, "mptp_summary.txt")

  @property
  def mptp_output_summary_all_rootings(self):
    return os.path.join(self.species_delimitation_dir, "mptp_summary_all_rootings.txt")

  @property
  def mptp_output_summary_all_rootings_one_histogram(self):
    return os.path.join(self.species_delimitation_dir, "mptp_summary_all_rootings_one_histogram.txt")

  @property
  def raxml_all_ml_trees_ll(self):
    return os.path.join(self.likelihoods_dir, "all_ml_trees_with_likelihood.txt")

  @property
  def raxml_iqtree_ll(self):
    return os.path.join(self.likelihoods_dir, "raxml_iqtree_ll.txt")

  @property
  def raxml_iqtree_ll_all(self):
    return os.path.join(self.likelihoods_dir, "raxml_iqtree_ll_all.csv")

  @property
  def gamma_ll_all(self):
    return os.path.join(self.likelihoods_dir, "gamma_ll_all.csv")

  @property
  def gamma_median_ll_all(self):
    return os.path.join(self.likelihoods_dir, "gamma_median_ll_all.csv")

  @property
  def raxmlng_param_jiggle_llhs(self):
    return os.path.join(self.likelihoods_dir, "raxmlng_param_jiggle_llhs.csv")

  @property
  def iqtree_param_jiggle_llhs(self):
    return os.path.join(self.likelihoods_dir, "iqtree_param_jiggle_llhs.csv")

  @property
  def ss_mre_thinned_tree(self):
    return os.path.join(self.thinning_dir, "ss_mre_thinned_tree.newick")
  
  @property
  def cc_thinned_alignment(self):
    return os.path.join(self.thinning_dir, "clade_compression_thinned_alignment.fasta")

  @property
  def me_thinned_alignment(self):
    return os.path.join(self.thinning_dir, "max_entropy_thinned_alignment.fasta")

  @property
  def rand_thinned_alignment(self):
    return os.path.join(self.thinning_dir, "random_thinned_alignment.fasta")

  @property
  def leaves_thinned_tree(self):
    return os.path.join(self.thinning_dir, "leaves_thinned_tree.newick")

  @property
  def root_digger_output(self):
    return os.path.join(self.rootdigger_dir, "root_digger_lwr.newick")

  @property
  def root_digger_output_csv(self):
    return os.path.join(self.rootdigger_dir, "root_digger_lwr.csv")

  @property
  def root_digger_logfile(self):
    return os.path.join(self.rootdigger_dir, "root_digger.log")

  _version = "UNDEFINED"


# misc
subst_model = "GTR+FO+G4"
raxml_precision = "9"
raxml_min_bl = "0.000000001"

pargenes_seed = 3000
pargenes_rand_trees = 50
pargenes_pars_trees = 50
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
