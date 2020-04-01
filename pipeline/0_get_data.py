#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import subprocess
import data_versioning
import re

if len(sys.argv) != 2:
	print "Please supply Google Drive link to the file."
	sys.exit(1)

drive_link = sys.argv[1]

possible_id = re.search('/d/(.+?)/view?', drive_link)
if not possible_id:
	print "Drive Link looks wrong: ", drive_link
	sys.exit(1)
else:
	data_googleid = possible_id.group(1)

data_versioning.setup_new_version()

cmd = []
cmd.append("wget")
cmd.append("--no-check-certificate")
cmd.append("https://docs.google.com/uc?export=download&id=" + data_googleid)
cmd.append("-O")
cmd.append(common.raw_alignment)
print(" ".join(cmd))
subprocess.call(cmd)
