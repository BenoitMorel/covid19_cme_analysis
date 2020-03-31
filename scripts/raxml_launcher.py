import os
import sys
import launcher
import common


def launch_raxml(alignment, model, output_dir, seed, starting_trees = 1, parsimony = False, bs_trees = 0, cores = 16, debug = False, parse = False):
  try:
    os.mkdir(output_dir)
  except:
    pass
  prefix = os.path.join(output_dir, "raxml" ) 
  prefix += "_" + model.replace("+","")
  cmd = []
  cmd.append("mpiexec")
  cmd.append("-np")
  cmd.append(str(cores))
  cmd.append(common.raxml)
  cmd.append("--msa")
  cmd.append(alignment)
  cmd.append("--model")
  cmd.append(model)
  cmd.append("--seed")
  cmd.append(str(seed))
  cmd.append("--blmin")
  cmd.append(common.raxml_min_bl)
  if (parse):
    cmd.append("--parse")
  cmd.append("--tree")
  if (starting_trees > 0):
    if (not parsimony):
      cmd.append("rand{" + str(starting_trees) + "}")
      prefix += "_rand" + str(starting_trees)
    else:
      cmd.append("pars{" + str(starting_trees) + "}")
      prefix += "_pars" + str(starting_trees)
  if (bs_trees > 0):
    cmd.append("--boostrap")
    cmd.append("--bs-trees")
    cmd.append(str(bs_trees))
    prefix += "_bs" + str(bs_trees)

  prefix += "_seed" + str(seed)
  cmd.append("--prefix")
  cmd.append(prefix)
  launcher.submit_haswell(prefix, cmd, cores, debug) 
