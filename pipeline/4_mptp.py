#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import pargenes_launcher
import mptp_launcher
import util

version = util.get_version( sys.argv )

tree = util.versioned_path( version, common.raxml_best_tree)
output = util.versioned_path( version, common.mptp_output )
mptp_launcher.launch_mptp(tree, output)

