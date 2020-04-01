#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import export_best_raxml_run
import util

version = util.get_version( sys.argv )

raxml_ml_runs_dir = util.versioned_path( version, common.raxml_ml_runs_dir )
raxml_best_ml_run_dir = util.versioned_path( version, common.raxml_best_ml_run_dir )

pattern = os.path.join(raxml_ml_runs_dir, "*raxml.log")
export_best_raxml_run.export(pattern, raxml_best_ml_run_dir)
