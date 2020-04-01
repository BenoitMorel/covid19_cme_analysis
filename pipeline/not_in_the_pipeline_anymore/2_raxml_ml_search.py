#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import raxml_launcher
import common
import util

version = util.get_version( sys.argv )

cores = common.cores_for_one_raxml_run
alignment = util.versioned_path( version, common.alignment )

output_dir = util.versioned_path( version, os.path.join("runs", "raxml_runs") )
for seed in range(1005, 1020):
  raxml_launcher.launch_raxml(alignment, common.subst_model, output_dir, seed, parsimony = False, cores = cores)

for seed in range(2005, 2020):
  raxml_launcher.launch_raxml(alignment, common.subst_model, output_dir, seed, parsimony = True, cores = cores)



if (False):
  for seed in range(1000, 1005):
    raxml_launcher.launch_raxml(alignment, common.subst_model, output_dir, seed, parsimony = False, cores = cores)

  for seed in range(2000, 2005):
    raxml_launcher.launch_raxml(alignment, common.subst_model, output_dir, seed, parsimony = True, cores = cores)






