#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import remove_duplicates
import util

version = util.get_version( sys.argv )

raw_alignment = util.versioned_path( version, common.raw_alignment )
alignment = util.versioned_path( version, common.alignment )
outgroup_alignment = util.versioned_path( version, common.outgroup_alignment )
duplicates = util.versioned_path( version, common.duplicates_json)

remove_duplicates.remove_duplicates( raw_alignment, common.outgroup_spec, alignment, duplicates, outgroup_alignment )
