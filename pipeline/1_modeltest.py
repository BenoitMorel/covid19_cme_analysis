#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import modeltest_launcher
import common

cores = 16
output_dir = os.path.join("runs", "modeltest_runs")
seed = 20

modeltest_launcher.launch_modeltest(common.alignment, output_dir, seed = seed, cores = cores)






