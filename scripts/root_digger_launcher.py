import os
import sys
import launcher
import common
import subprocess
import util


def launch_root_digger(tree,
                       alignment,
                       model,
                       prefix,
                       logfile,
                       cores,
                       factor="1e20"):
    cmd = []
    #cmd.extend["mpiexec"]
    #cmd.extend(["-np", cores])
    cmd.extend([common.root_digger])
    cmd.extend(["--tree", tree])
    cmd.extend(["--msa", alignment])
    cmd.extend(["--model", model])
    cmd.extend(["--exhaustive"])
    cmd.extend(["--prefix", prefix])
    cmd.extend(["--early-stop"])
    cmd.extend(["--threads"])
    #cmd.extend(["--verbose"])
    print(cmd)
    with open(logfile, 'w') as outfile:
        subprocess.check_call(cmd, stdout=outfile, stderr=outfile)
