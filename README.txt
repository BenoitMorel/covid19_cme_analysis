

Usage:
Install required tools with
./setup.sh

Run the pipeline by calling the scripts in the pipeline directory.
- if you are on the HITS internal cluster, some of the scripts will submit jobs
- else, the scripts will run normally on your machine

Everytime you call the 0_get_data.py script, a new version of the data, the runs and the results will be created, and the previous ones will be backuped. 

There are several parameters that can be set in scripts/common.py.
TODO: Some of them should be handled differently, in a configuration file.

Requirements:
bison, flex, MPI, python (with package ete3)

