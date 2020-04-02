

Usage:

All scripts should be ran from the repository root directory.

Install required tools with
`./setup.sh`


Run the pipeline by calling the scripts that are located in the pipeline directory.
- if you are on the HITS internal cluster, some of the scripts will submit jobs
- else, the scripts will run normally on your machine

The first script needs a link to an alignment located in google drive. For instance (with a fake link):
`./pipeline/0_get_data.py https://drive.google.com/file/d/somegoogleID/view`
It will create a directory, for instance: `work_dir/2020-04-01_00/`
Then, to run one of the following scripts on this data, use:
`./pipeline/1_scriptname.py 2020-04-01_00`

Several parameters can be set in scripts/common.py.
TODO: Some of them should be handled differently, in a configuration file.

Requirements:
bison, flex, MPI, python, GSL

