#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import remove_duplicates

remove_duplicates.remove_duplicates(common.raw_alignment, common.alignment)

