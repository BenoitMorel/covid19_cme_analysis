import os
import sys
import shutil
import glob
import common
import datetime
import util

def relative_symlink(src, dest):
  relative_path = os.path.relpath(src, os.path.dirname(dest))
  tmp = dest + ".sym"
  os.symlink(relative_path,  tmp)
  shutil.move(tmp, dest)

def get_current_version_id( date ):
  pattern = os.path.join(common.work_dir, date + r"_[0-9][0-9]")
  files = glob.glob(pattern)
  # print(files)
  return str(len(files)).zfill(2)

def setup_directory(directory, subdirectory, version):
  real_current = os.path.join(directory, version, subdirectory)
  util.make_path(real_current)

def setup_new_dataset(path):
  util.make_path(path.root_data_dir)
  util.make_path(path.root_runs_dir)
  util.make_path(path.root_results_dir)


def setup_new_version( date=datetime.datetime.now().strftime("%Y-%m-%d"),
    datasets = ["fmsao", "fmsan", "smsao", "smsan"]):

  version_id = get_current_version_id( date )

  version = "{}_{}".format( date, version_id )

  # make the base path for the version
  util.make_path( util.versioned_path(version, "") )

  # generate the appropriate paths
  paths = []
  for ds in datasets:
    p = common.Paths([version, ds], 0)
    setup_new_dataset(p)
    paths.append(p)

  print(version)

  return paths
