#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import remove_duplicates
import remove_outgroups
import util

version = util.get_version( sys.argv )

raw_alignment = util.versioned_path( version, common.raw_alignment )
alignment = util.versioned_path( version, common.alignment )

if (common.remove_duplicates):
  remove_duplicates.remove_duplicates( raw_alignment, alignment)
if (len(common.outgroups_to_remove)):
  remove_outgroups.remove_outgroups(alignment, alignment, common.outgroups_to_remove)


