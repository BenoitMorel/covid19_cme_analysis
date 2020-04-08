#!/usr/bin/env python
import os
import sys
sys.path.insert(0, 'scripts')
import common
import compare_llhs
paths = common.Paths( sys.argv )

compare_llhs.evaluate_all_trees(paths)
