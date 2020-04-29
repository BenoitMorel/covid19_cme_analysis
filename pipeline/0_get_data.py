#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, 'scripts')
import common
import subprocess
import data_versioning
import re
import util
import dl_gdrive

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

# only dl the data once
p = paths[0]:
"""
cmd = []
cmd.append("wget")
cmd.append("--no-check-certificate")
cmd.append("https://docs.google.com/uc?export=download&id=" + data_googleid)
cmd.append("-O")
cmd.append( p.raw_sequences + ".gz" )
print(" ".join(cmd))
subprocess.call(cmd)
"""

print("Downloading the data")
dl_gdrive.download_file_from_google_drive(data_googleid, p.raw_sequences + ".gz")

print("")
print("Version string: " + p.version)

# if remote was gzipped
if True:
  cmd = []
  cmd.append("gunzip")
  cmd.append( p.raw_sequences+ ".gz" )
  print((" ".join(cmd)))
  subprocess.call(cmd)

