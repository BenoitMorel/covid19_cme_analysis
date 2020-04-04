#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import root_digger_launcher

paths = common.Paths(sys.argv)

tree = paths.raxml_best_tree
alignment = paths.alignment
outfile = paths.root_digger_output
logfile = paths.root_digger_logfile
cores = str(common.available_cores//2)
model = common.subst_model

root_digger_launcher.launch_root_digger(tree, alignment, model,
		outfile, logfile, cores)
