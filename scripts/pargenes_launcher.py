import os
import sys
import launcher
import shutil
import common

  
def relative_symlink(src, dest):
  relative_path = os.path.relpath(src, os.path.dirname(dest))
  tmp = dest + ".sym"
  os.symlink(relative_path,  tmp)
  shutil.move(tmp, dest)


def launch_pargenes(alignment, model, output_dir, seed, rand_trees, pars_trees, bs_trees, cores):
  try:
    os.mkdir(output_dir)
  except:
    pass
  debug = False 
  run_name = "pargenes_" + model.replace("+","") + "_r" + str(rand_trees) + "_p" + str(pars_trees) + "_bs" + str(bs_trees) + "_seed" + str(seed)
  run_dir = os.path.join(output_dir, run_name)
  os.mkdir(run_dir)
  alignment_dir = os.path.join(run_dir, "alignments")
  os.mkdir(alignment_dir)
  alignment_symlink = os.path.join(alignment_dir, "ali.fasta")
  raxml_options_file = os.path.join(run_dir, "raxml_options.txt")
  with open(raxml_options_file, "w") as writer:
    writer.write("--model " + model + " ")
    writer.write("--blmin " + common.raxml_min_bl + " ")
    writer.write("--precision " + str(common.raxml_precision) + " ")

  relative_symlink(alignment, alignment_symlink) 
  prefix = os.path.join(run_dir, "pargenes") 
  cmd = []
  cmd.append("python")
  cmd.append(common.pargenes)
  cmd.append("-a")
  cmd.append(alignment_dir)
  cmd.append("-o")
  cmd.append(os.path.join(run_dir, "pargenes_run"))
  cmd.append("-r")
  cmd.append(raxml_options_file)
  cmd.append("--seed")
  cmd.append(str(seed))
  cmd.append("-s")
  cmd.append(str(rand_trees))
  cmd.append("-p")
  cmd.append(str(pars_trees))
  cmd.append("-b")
  cmd.append(str(bs_trees))
  cmd.append("-c")
  cmd.append(str(cores))
  print(" ".join(cmd))
  launcher.submit(prefix, cmd, cores, debug) 



#python software/ParGenes/pargenes/pargenes-hpc.py  -a plop -o output_plop -d nt -c 4 --raxml-global-parameters  global.txt  --dry-run -b 100 --seed
