#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'scripts')
import common
import export_pargenes_output

paths = common.Paths( sys.argv )

export_pargenes_output.export( paths.pargenes_runs_dir, paths )



