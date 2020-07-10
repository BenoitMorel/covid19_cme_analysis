
************
** Usage: **
************

All scripts should be ran from the repository root directory.

Install required tools with
`./setup.sh`


Run the pipeline by calling the scripts that are located in the pipeline directory.
- if you are on the HITS internal cluster, some of the scripts will submit jobs
- else, the scripts will run normally on your machine

The first script needs a link to an alignment located in google drive. For instance (with a fake link):
`./pipeline/0_get_data.py https://drive.google.com/file/d/somegoogleID/view`
It will create a directory structure, for instance: `work_dir/2020-04-01_00/`, followed by subdirectories for the different variants of the MSA (fmsao, fmsan, smsao, smsan).
Then, to run one of the following scripts on this data, use:
`./pipeline/1_scriptname.py 2020-04-01_00 fmsao`
(or whatever other MSA version )

Several parameters can be set in scripts/common.py.


**************************
** Directory  structure **
**************************

The pipeline produces files into work_dir.

Each directory under work_dir corresponds to a version (date of the snapshot), for instance 2020-05-05_00.

Each directory under a version corresponds to a dataset. All datasets under the same version are created from the same raw sequences, but with different filters (see the paper for a more detailed description).
- fmsao: Full MSA with outgroups
- fmsan: Full MSA without outgroups (fmsa in the paper) 
- smsao: Singleton-removed MSA with outgroups
- smsan: Singleton-removed MSA without outgroups (smsa in the paper)
- *-cc-thinned: Alignment obtained from Clade Compression thinning
- *-ss-thinned: Alignment obtained from Support Selection thinning

Each dataset contains 3 folders: 
- data, with the initial filtered alignment and a few more additional files
- runs, with the run directories of all steps of the pipeline
- results, with the most important results of the pipeline



