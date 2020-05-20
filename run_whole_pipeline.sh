#!/bin/bash

set -e
#pipeline/2_pargenes.py  $1 $2
#pipeline/3_export_pargenes_results.py  $1 $2
#pipeline/4_mptp.py  $1 $2
#pipeline/7_iqtree_tests.py  $1 $2
#pipeline/9_tree_thinning.py  $1 $2
pipeline/8_compare_llhs.py  $1 $2
#pipeline/5_epa_outgroup_rooting.py  $1 $2
pipeline/6_root_digger_rooting.py  $1 $2

