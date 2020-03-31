import os
import sys
import shutil
import glob
import common
import datetime

def relative_symlink(src, dest):
  relative_path = os.path.relpath(src, os.path.dirname(dest))
  tmp = dest + ".sym"
  os.symlink(relative_path,  tmp)
  shutil.move(tmp, dest)

def get_current_version_id():
  pattern = os.path.join(common.root_data_dir, "[0123456789]*_covid_*")
  files = glob.glob(pattern)
  print(files)
  if (len(files) == 0):
    return "00"
  id_len = 2
  max_id = 0
  for f in files:
    f = os.path.basename(f)
    max_id = max(max_id, int(f[:2]))
  max_id += 1
  res = "0" * (id_len - len(str(max_id))) + str(max_id)
  return res

def setup_directory(directory, current, version):
  real_current = os.path.join(directory, version)
  os.mkdir(real_current)
  try:
    os.remove(current)
  except:
    pass
  relative_symlink(real_current, current)

def setup_new_version():
  version_id = get_current_version_id()
  version = version_id + "_covid"
  now = datetime.datetime.now()
  version += "_" + str(now.year)  + str(now.month) + str(now.day)
  setup_directory(common.root_data_dir, common.data_path, version)
  setup_directory(common.root_runs_dir, common.runs_dir, version)
  setup_directory(common.root_results_dir, common.results_dir, version)
  print(version)
 

