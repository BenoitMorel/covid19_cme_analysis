import os
import glob
import shutil


def get_loglikelihood(raxml_log_file):
  for line in open(raxml_log_file).readlines():
    if (line.startswith("Final LogLikelihood:")):
      return float(line.split(" ")[2][:-1])
  return 0.0


def export(pattern, output_dir):
  try:
    os.mkdir(output_dir)
  except:
    pass
  runs = []
  for logfile in glob.glob(pattern):
    ll = get_loglikelihood(logfile)
    if (ll != 0.0):
      runs.append((ll, logfile))
  runs.sort()
  for run in runs:
    print(str(run[0]) + " " + run[1])
  
  if (len(runs) == 0):
    print("[Error] No finished raxml run found in " + pattern)
    return
  best_run_prefix = runs[-1][1].replace("raxml.log", "")
  print("Exporting best run file into " + output_dir + ":")
  for filetocp in glob.glob(best_run_prefix + "*"):
    dest = os.path.join(output_dir, "bestrun.raxml." + filetocp.split(".raxml.")[1])
    print("  Exporting " + filetocp + " to " + dest)
    shutil.copy(filetocp, dest)
  

