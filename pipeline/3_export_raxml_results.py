#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import export_best_raxml_run

pattern = os.path.join(common.raxml_ml_runs_dir, "*raxml.log")
export_best_raxml_run.export(pattern, common.raxml_best_ml_run_dir)

