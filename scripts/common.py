#!/usr/bin/env python

import os

# tools
software_path = "software"
raxml = os.path.join(software_path, "raxml-ng", "bin", "raxml-ng-mpi")
modeltest = os.path.join(software_path, "modeltest", "bin", "modeltest-ng-mpi")
pargenes = os.path.join(software_path, "ParGenes", "pargenes", "pargenes-hpc.py")

# data
data_googleid = "1LpC3kmBh52vOrnpOMhGF7zMNTz0Ll6fF"
data_path = os.path.join("data", "current")
alignment = os.path.join(data_path, "covid_edited.fasta")


# runs
runs_dir = os.path.join("runs", "current")

raxml_ml_runs_dir = os.path.join(runs_dir, "raxml_runs")
pargenes_runs_dir = os.path.join(runs_dir, "pargenes_runs")
modeltest_runs_dir = os.path.join(runs_dir, "modeltest_runs")

# results
results_dir = os.path.join("results", "current")
raxml_best_ml_run_dir = os.path.join(results_dir, "best_raxml_run")

# misc
subst_model = "GTR+R4"
raxml_min_bl = "1e-9"


