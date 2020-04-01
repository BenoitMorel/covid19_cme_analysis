#!/usr/bin/env python
import os
import sys
sys.path.insert(0, 'scripts')
import common
import util
import export_pargenes_output

version = util.get_version( sys.argv )
pargenes_dir = util.versioned_path( version, common.pargenes_runs_dir )
export_pargenes_output.export(pargenes_dir, version)

