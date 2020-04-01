#!/usr/bin/env python

import os

scripts_dir = os.path.dirname( os.path.realpath(__file__) )
base_dir = os.path.abspath( os.path.realpath( os.path.join(
            os.path.dirname( os.path.abspath( os.path.realpath( __file__ ))),
            "..")))
work_dir = os.path.join(base_dir, "work_dir")

# tools
software_path = os.path.join(base_dir, "software")
raxml = os.path.join(software_path, "raxml-ng", "bin", "raxml-ng-mpi")
modeltest = os.path.join(software_path, "modeltest", "bin", "modeltest-ng-mpi")
pargenes = os.path.join(software_path, "ParGenes", "pargenes", "pargenes-hpc.py")
mptp = os.path.join(software_path, "mptp", "bin", "mptp")
epa = os.path.join(software_path, "epa-ng", "bin", "epa-ng")

# data
root_data_dir = "data"
data_path = os.path.join(root_data_dir)
raw_alignment = os.path.join(data_path, "covid_raw.fasta")
alignment = os.path.join(data_path, "covid_edited.fasta")

# runs
root_runs_dir = "runs"
runs_dir = os.path.join(root_runs_dir)
raxml_ml_runs_dir = os.path.join(runs_dir, "raxml_runs")
pargenes_runs_dir = os.path.join(runs_dir, "pargenes_runs")
modeltest_runs_dir = os.path.join(runs_dir, "modeltest_runs")

# results
root_results_dir = "results"
results_dir = os.path.join(root_results_dir)
raxml_best_tree = os.path.join(results_dir, "raxml_best_tree.newick")
raxml_best_model = os.path.join(results_dir, "raxml_best_model.txt")
raxml_all_ml_trees = os.path.join(results_dir, "raxml_all_ml_trees.newick")
raxml_all_ml_trees_ll = os.path.join(results_dir, "raxml_all_ml_trees_with_ll.txt")
raxml_bootstrap_trees = os.path.join(results_dir, "raxml_bs_trees.newick")

mptp_output = os.path.join(results_dir, "mptp_output.txt")

# misc
subst_model = "GTR+R4"
remove_duplicates = True
outgroups_to_remove = ["BAT", "PANGOLIN"]
raxml_precision = "9"
raxml_min_bl = "0.000000001"
 
pargenes_seed = 3000
pargenes_rand_trees = 0
pargenes_pars_trees = 100
pargenes_bs_trees = 100

available_cores = 4
cores_for_one_raxml_run = 4


