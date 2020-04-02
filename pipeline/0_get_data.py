#!/usr/bin/env python

import os
import sys
sys.path.insert(0, 'scripts')
import common
import subprocess
import data_versioning
import re
import util

if len(sys.argv) != 2:
	util.fail("Please supply Google Drive link to the file.")

drive_link = sys.argv[1]

if "drive.google.com/file/d/" in drive_link:
	pattern = r'/d/(.+?)/view?'
elif "drive.google.com/open?id=" in drive_link:
	pattern = r'id=(.+?)$'
else:
	util.fail("Drive Link looks wrong: {}".format(drive_link) )

possible_id = re.search(pattern, drive_link)
if not possible_id:
	util.fail("Drive Link looks wrong after pattern: {}".format(drive_link) )
else:
	data_googleid = possible_id.group(1)
	data_googleid.rstrip()

paths = data_versioning.setup_new_version()

cmd = []
cmd.append("wget")
cmd.append("--no-check-certificate")
cmd.append("https://docs.google.com/uc?export=download&id=" + data_googleid)
cmd.append("-O")
cmd.append( paths.raw_alignment )
print(" ".join(cmd))
subprocess.call(cmd)
print("")
print("Version string: " + paths.version)



