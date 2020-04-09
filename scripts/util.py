from shutil import rmtree
import os
import sys
import common
import subprocess

def fail( msg ):
	print( msg )
	sys.exit(1)

def versioned_path(version, path):
	return os.path.join( common.work_dir, version, path)

def version_valid( version ):
	return os.path.isdir( versioned_path( version, "" ) )

def get_version( argv, i=1 ):
	if len(argv) < i+1:
		fail("Insufficient arguments (version string?)")
	version = argv[i]
	if not version_valid( version ):
		fail("Invalid version: {}".format(version))
	return version

def clean_dir( path ):
	if os.path.exists( path ):
		rmtree( path, ignore_errors=True )

def clean_file ( path ):
  if os.path.exists( path ):
    os.remove( path )

def mkdirp( path ):
	if not os.path.exists( path ):
		os.mkdir( path )

def make_path( path ):
	if not os.path.exists( path ):
		os.makedirs( path )

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
