#!/usr/bin/env python

import os

# tools
software_path = "software"
raxml = os.path.join(software_path, "raxml-ng", "bin", "raxml-ng-mpi")
modeltest = os.path.join(software_path, "modeltest", "bin", "modeltest-ng-mpi")
pargenes = os.path.join(software_path, "ParGenes", "pargenes", "pargenes-hpc.py")
mptp = os.path.join(software_path, "mptp", "bin", "mptp")
epa = os.path.join(software_path, "epa-ng", "bin", "epa-ng")

# data
data_googleid = "1LpC3kmBh52vOrnpOMhGF7zMNTz0Ll6fF"
root_data_dir = "data"
data_path = os.path.join(root_data_dir, "current")
raw_alignment = os.path.join(data_path, "covid_raw.fasta")
alignment = os.path.join(data_path, "covid_edited.fasta")

# runs
root_runs_dir = "runs"
runs_dir = os.path.join(root_runs_dir, "current")
raxml_ml_runs_dir = os.path.join(runs_dir, "raxml_runs")
pargenes_runs_dir = os.path.join(runs_dir, "pargenes_runs")
modeltest_runs_dir = os.path.join(runs_dir, "modeltest_runs")

# results
root_results_dir = "results"
results_dir = os.path.join(root_results_dir, "current")
raxml_best_ml_run_dir = os.path.join(results_dir, "best_raxml_run")
raxml_best_ml_tree = os.path.join(raxml_best_ml_run_dir, "bestrun.raxml.bestTree")
mptp_output = os.path.join(results_dir, "mptp_output.txt")

# misc
subst_model = "GTR+R4"
remove_duplicates = True
outgroups_to_remove = ["BAT", "PANGOLIN"]
raxml_min_bl = "1e-9"
available_cores = 128
cores_for_one_raxml_run = 4


