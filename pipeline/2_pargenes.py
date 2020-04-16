#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import pargenes_launcher

paths = common.Paths( sys.argv )

alignment = paths.alignment
model = common.subst_model
output_dir = paths.pargenes_runs_dir
seed = common.pargenes_seed
rand_trees = common.pargenes_rand_trees
pars_trees = common.pargenes_pars_trees
bs_trees = common.pargenes_bs_trees
cores = common.available_cores

pargenes_launcher.launch_pargenes(alignment, model, output_dir, seed, rand_trees, pars_trees, bs_trees, cores)

