import os
import sys
import launcher
import common
import subprocess
import util

def launch_epa(tree, modelfile, ref_msa, query_msa, out_dir, thorough=True):
  util.make_path(out_dir)

  cmd = []
  cmd.append(common.epa)
  cmd.append("--tree")
  cmd.append(tree)
  cmd.append("--model")
  cmd.append(modelfile)
  cmd.append("--msa")
  cmd.append(ref_msa)
  cmd.append("--query")
  cmd.append(query_msa)
  cmd.append("--threads")
  cmd.append("4")
  if thorough:
  	cmd.append("--no-heur")
  cmd.append("--filter-max")
  cmd.append("50")
  cmd.append("--filter-acc-lwr")
  cmd.append("1.0")
  cmd.append("--out-dir")
  cmd.append(out_dir)
  cmd.append("--redo")
  cmd.append("--verbose")
  subprocess.check_call(cmd)

def launch_split4epa(ref_phylip, papara_result, out_dir):
  util.make_path(out_dir)

  cmd = []
  cmd.append(common.epa)
  cmd.append("--split")
  cmd.append(ref_phylip)
  cmd.append(papara_result)
  cmd.append("--out-dir")
  cmd.append(out_dir)
  cmd.append("--redo")
  subprocess.check_call(cmd)

  return os.path.join(out_dir, "reference.fasta"), os.path.join(out_dir, "query.fasta")

def launch_papara(tree, ref_phylip, query_fasta, out_dir):
  util.make_path(out_dir)

  name = "aln"

  cmd = []
  cmd.append(common.papara)
  cmd.append("-t")
  cmd.append(tree)
  cmd.append("-s")
  cmd.append(ref_phylip)
  cmd.append("-q")
  cmd.append(query_fasta)
  cmd.append("-j")
  cmd.append("4")
  cmd.append("-r")
  cmd.append("-n")
  cmd.append(name)
  subprocess.check_call(cmd, cwd=out_dir)

  return os.path.join( out_dir, "papara_alignment." + name )
