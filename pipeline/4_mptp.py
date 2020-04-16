#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import pargenes_launcher
import mptp_launcher

paths = common.Paths( sys.argv )

tree = paths.raxml_best_tree
output = paths.mptp_output
mptp_launcher.launch_mptp_mcmc(tree, output)

