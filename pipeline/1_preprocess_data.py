#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import remove_duplicates
import remove_outgroups


if (common.remove_duplicates):
  remove_duplicates.remove_duplicates(common.raw_alignment, common.alignment)
if (len(common.outgroups_to_remove)):
  remove_outgroups.remove_outgroups(common.alignment, common.alignment, common.outgroups_to_remove)


