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
outgroup_alignment = util.versioned_path( version, common.outgroup_alignment )
duplicates = util.versioned_path( version, common.duplicates_json)

# raw_alignment_no_outgroup = alignment + ".nooutgroup"


# remove_outgroups.remove_outgroups(raw_alignment, raw_alignment_no_outgroup, common.outgroups_to_remove)
    
remove_duplicates.remove_duplicates( raw_alignment, common.outgroup_spec, alignment, duplicates, outgroup_alignment )

# util.clean_file(raw_alignment_no_outgroup)


