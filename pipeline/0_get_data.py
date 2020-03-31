#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import subprocess
import data_versioning


data_versioning.setup_new_version()

cmd = []
cmd.append("wget")
cmd.append("--no-check-certificate")
cmd.append("https://docs.google.com/uc?export=download&id=" + common.data_googleid)
cmd.append("-O")
cmd.append(common.raw_alignment)
print(" ".join(cmd))
subprocess.call(cmd)



