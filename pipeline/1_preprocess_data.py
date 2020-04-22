#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import remove_duplicates
import util

paths = common.Paths( sys.argv )

remove_duplicates.trim_separate_align(  paths.raw_sequences,
                                        paths.version,
                                        paths.preanalysis_runs_dir )

result_file=os.path.join( paths.preanalysis_runs_dir, "{}_nooutgroup_trimmed_nosingle.aln".format( paths.version ) )
util.expect_file_exists( result_file )
util.copy( result_file, paths.raw_alignment )

remove_duplicates.remove_duplicates(paths.raw_alignment,
									common.outgroup_spec,
									paths.alignment,
									paths.duplicates_json,
									paths.outgroup_alignment )
