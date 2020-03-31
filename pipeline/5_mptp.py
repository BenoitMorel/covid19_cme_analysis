#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import pargenes_launcher

tree = common.raxml_best_ml_tree
output = common.mptp_output
mptp_launcher.launch_mptp(tree, output)

