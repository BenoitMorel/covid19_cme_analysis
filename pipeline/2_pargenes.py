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
seed = 3000
rand_trees = 0
pars_trees = 100
bs_trees = 100
cores = common.available_cores

pargenes_launcher.launch_pargenes(alignment, model, output_dir, seed, rand_trees, pars_trees, bs_trees, cores)


