#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import raxml_launcher
import common

cores = 16
output_dir = os.path.join("runs", "raxml_runs")
for seed in range(1005, 1020):
  raxml_launcher.launch_raxml(common.alignment, common.subst_model, output_dir, seed, parsimony = False, cores = cores)

for seed in range(2005, 2020):
  raxml_launcher.launch_raxml(common.alignment, common.subst_model, output_dir, seed, parsimony = True, cores = cores)



if (False):
  for seed in range(1000, 1005):
    raxml_launcher.launch_raxml(common.alignment, common.subst_model, output_dir, seed, parsimony = False, cores = cores)

  for seed in range(2000, 2005):
    raxml_launcher.launch_raxml(common.alignment, common.subst_model, output_dir, seed, parsimony = True, cores = cores)






