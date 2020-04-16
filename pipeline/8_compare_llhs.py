#!/usr/bin/env python
import os
import sys
sys.path.insert(0, 'scripts')
import common
import compare_llhs
import jiggle_params
paths = common.Paths( sys.argv )

#compare_llhs.evaluate_all_trees(paths)
jiggle_params.evaluate_all(paths)
