import os
import sys
import shutil
import subprocess

import common
import util

def convert(in_type, out_type, in_file, out_file):
  util.expect_file_exists( in_file )
  util.clean_file(out_file)

  cmd = []
  cmd.append(common.genesis_convert)
  cmd.append(in_type)
  cmd.append(out_type)
  cmd.append(in_file)
  cmd.append(out_file)
  subprocess.check_call(cmd)
