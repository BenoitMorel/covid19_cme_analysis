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
import binascii

def is_gz_file(filepath):
    with open(filepath, 'rb') as test_f:
        return binascii.hexlify(test_f.read(2)) == b'1f8b'

if len(sys.argv) != 2:
	util.fail("Please supply local path or Google Drive link to the sequence file.")

given_path = sys.argv[1]
local=False
if "drive.google.com/file/d/" in given_path:
	pattern = r'/d/(.+?)/view?'
elif "drive.google.com/open?id=" in given_path:
	pattern = r'id=(.+?)$'
elif os.path.isfile( given_path ):
  local=True
else:
	util.fail("Given path must either be a local path or a google drive link: {}".format(given_path) )

if not local:
  possible_id = re.search(pattern, given_path)
  if not possible_id:
  	util.fail("Drive Link looks wrong after pattern: {}".format(given_path) )
  else:
  	data_googleid = possible_id.group(1)
  	data_googleid.rstrip()

paths = data_versioning.setup_new_version()

# only dl the data once
p = paths[0]
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


if not local:
  print("Downloading the data")
  given_path="tmp_file.msa"
  dl_gdrive.download_file_from_google_drive( data_googleid, tmp_file )

# if remote was gzipped
was_gz = False
if is_gz_file( given_path ):
  was_gz = True
  print("Input was zipped. unzipping!")
  suffix="." + given_path.split('.')[-1]

  cmd = []
  cmd.append("gunzip")
  cmd.append("--keep")
  cmd.append("--suffix")
  cmd.append(suffix)
  cmd.append( given_path )
  #print((" ".join(cmd)))
  subprocess.call(cmd)

  given_path=given_path[:-len(suffix)]

if was_gz or not local:
  print("Moving the data over:\n  " + given_path + " -> " + p.raw_sequences)
  util.move( given_path, p.raw_sequences )
else:
  print("Making a copy of the data:\n  " + given_path + " -> " + p.raw_sequences)
  util.copy( given_path, p.raw_sequences )

print("")
print("Version string: " + p.version)
