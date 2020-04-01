#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import pargenes_launcher
import util

version = util.get_version( sys.argv )

alignment = util.versioned_path( version, common.alignment )
model = common.subst_model
output_dir = util.versioned_path( version, common.pargenes_runs_dir )
seed = common.pargenes_seed
rand_trees = common.pargenes_rand_trees
pars_trees = common.pargenes_pars_trees
bs_trees = common.pargenes_bs_trees
cores = common.available_cores

pargenes_launcher.launch_pargenes(alignment, model, output_dir, seed, rand_trees, pars_trees, bs_trees, cores)

