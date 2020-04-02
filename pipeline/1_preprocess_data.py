#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import remove_duplicates

paths = common.Paths( sys.argv )

remove_duplicates.remove_duplicates(paths.raw_alignment,
									common.outgroup_spec,
									paths.alignment,
									paths.duplicates_json,
									paths.outgroup_alignment )
