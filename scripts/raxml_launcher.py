import os
import sys
import launcher
import common
import util
import subprocess as sub


def launch_raxml(alignment, model, output_dir, seed, starting_trees = 1, parsimony = False, bs_trees = 0, cores = 16, debug = False, parse = False):
  util.expect_file_exists(alignment)
  util.make_path(output_dir)

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
  launcher.submit(prefix, cmd, cores, debug)

def evaluate(tree_file, ref_msa, out_dir):
  util.expect_file_exists(tree_file)
  util.expect_file_exists(ref_msa)
  util.make_path(out_dir)

  prefix = "eval"

  cmd = []
  cmd.append(common.raxml)
  cmd.append('--evaluate')
  cmd.append('--msa')
  cmd.append(ref_msa)
  cmd.append('--model')
  cmd.append(common.subst_model)
  cmd.append('--tree')
  cmd.append(tree_file)
  cmd.append('--prefix')
  cmd.append(prefix)
  cmd.append('--threads')
  cmd.append(str(common.iqtree_threads))
  cmd.append('--blopt')
  cmd.append('nr_safe')
  cmd.append('--redo')
  cmd.append("--blmin")
  cmd.append(common.raxml_min_bl)

  sub.check_call(cmd, cwd=out_dir, stdout=sub.DEVNULL)

  modelfile = os.path.join( out_dir, prefix + ".raxml.bestModel" )

  return modelfile
