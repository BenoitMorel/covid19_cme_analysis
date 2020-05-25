from shutil import rmtree, copyfile, copytree
import os
import sys
import stat
import common
import subprocess

def fail( msg ):
  print( msg )
  sys.exit(1)

def versioned_path(version, path):
  return os.path.join( common.work_dir, version, path)

def make_path_in_workdir(*items):
  return os.path.join( common.work_dir, *items)

def version_valid( version ):
  return os.path.isdir( versioned_path( version, "" ) )

def splitpath(path, maxdepth=20):
  path = os.path.normpath(path) 
  ( head, tail ) = os.path.split(path)
  return splitpath(head, maxdepth - 1) + [ tail ] if maxdepth and head and head != path else [ head or tail ]

# awful hack to allow calling 
# ./pipeline step.py work_dir/2020-05-05/smsan
def preprocess_argv( argv, i ):
  if len(argv) == i + 1:
    sp = splitpath(argv[i])
    if (os.path.abspath(sp[0]) == common.work_dir):
      res = [""] * i
      res.append(sp[1])
      res.append(sp[2])
      return res
  return argv

def get_version( argv, i=1 ):
  if len(argv) < i+1:
    fail("Insufficient arguments (version string?)")
  version = argv[i]
  if not version_valid( version ):
    fail("Invalid version: {}".format(version))
  return version

def copy( src, dest ):
  copyfile( src, dest )

def copy_dir( src, dest, ignore=None ):
  if ignore:
    ign_f = shutil.ignore_patterns(*ignore)
  else:
    ign_f = None
  copytree( src, dest, ignore=ign_f )

def clean_dir( path ):
  if os.path.exists( path ):
    rmtree( path, ignore_errors=True )

def clean_file ( path ):
  if os.path.exists( path ):
    os.remove( path )

def chmod_path( path ):
  if not os.path.isdir( path ):
    raise RuntimeError( "Directory doesn't exist: " + path )
  else:
    os.chmod( path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )

def chmod_file( file_path ):
  if not os.path.isfile( file_path ):
    raise RuntimeError( "File doesn't exist: " + file_path )
  else:
    os.chmod( file_path, stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH|stat.S_IWOTH )

def mkdirp( path ):
  if not os.path.exists( path ):
    os.mkdir( path )
    chmod_path( path )

def make_path( path ):
  if not os.path.exists( path ):
    os.makedirs( path )
    chmod_path( path )

def make_path_clean( path ):
  clean_dir( path )
  make_path( path )

def expect_dir_exists( dir_path ):
  if not os.path.isdir( dir_path ):
    raise RuntimeError( "Directory doesn't exist: " + dir_path )

def expect_file_exists( file_path ):
  if not os.path.isfile( file_path ):
    raise RuntimeError( "File doesn't exist: " + file_path )

def expect_executable_exists( executable ):
  import distutils.spawn
  if not distutils.spawn.find_executable( executable ):
    raise RuntimeError( "Executable not found: " + executable )

"""
  returns the first occurence of the string matching
  .*${marker1}${input_str}${marker2}.*  (bash notation)

  the function does not check that such a string exists
"""
def find_string_between(input_str, marker1, marker2):
  start = input_str.find(marker1) + len(marker1)
  end = input_str.find(marker2, start)
  return input_str[start:end]

def is_slurm():
  try:
    subprocess.call(["sbatch", "-V"])
  except:
    return False
  return True

def num_pyhsical_cores():
  out = subprocess.check_output(['lscpu', '--parse=Core,Socket'], encoding = 'utf-8')
  out = out.split('\n')
  num_cores = len(
     dict.fromkeys(
       [line for line in out if not line.startswith('#') and line != '']
  ))
  return num_cores
