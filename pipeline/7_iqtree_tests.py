#!/usr/bin/env python
import os
import sys
sys.path.insert(0, 'scripts')
import common
import iqtree_tests

paths = common.Paths( sys.argv )

iqtree_tests.perform_all_tests(paths)
