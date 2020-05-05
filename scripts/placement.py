import os
import sys
import launcher
import common
import subprocess
import util

def split_alignment_outgroups(input_msa, outgroup_spec, out_dir):
  util.expect_file_exists( input_msa )
  util.expect_file_exists( outgroup_spec )
  util.make_path( out_dir )

  new_ref_msa="reference.fasta"
  query_msa="query.fasta"

  cmd = []
  cmd.append(common.genesis_remove_sequences)
  cmd.append(input_msa)
  cmd.append(outgroup_spec)
  cmd.append(new_ref_msa)
  cmd.append(query_msa)
  subprocess.check_call(cmd, cwd=out_dir)

  return os.path.join(out_dir, new_ref_msa), os.path.join(out_dir, query_msa)

def outgroup_check(jplace_files, out_dir):
  for f in jplace_files:
    util.expect_file_exists( f )
  util.make_path( out_dir )

  cmd = []
  cmd.append(common.outgroup_check)
  for f in jplace_files:
    cmd.append(f)

  outfile = os.path.join( out_dir, "outgroup_check.txt" )
  with open( outfile ) as logfile:
    subprocess.check_call(cmd, stdout=logfile)

  return outfile

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
  if not util.is_slurm():
    cmd.append(str(common.available_cores))
  else:
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
  subprocess.check_call(cmd, stdout=common.FNULL)

def launch_split4epa(ref_phylip, aln_result, out_dir):
  util.make_path(out_dir)

  cmd = []
  cmd.append(common.epa)
  cmd.append("--split")
  cmd.append(ref_phylip)
  cmd.append(aln_result)
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
  if not util.is_slurm():
    cmd.append("-j")
    cmd.append(str(common.available_cores))
  cmd.append("-r")
  cmd.append("-n")
  cmd.append(name)
  subprocess.check_call(cmd, cwd=out_dir)

  return os.path.join( out_dir, "papara_alignment." + name )

def launch_hmmbuild(ref_msa, out_dir):
  util.make_path(out_dir)

  ref_hmm="reference.hmm"

  cmd = []
  cmd.append( os.path.join(common.hmmer_dir, "hmmbuild") )
  if not util.is_slurm():
    cmd.append("--cpu")
    cmd.append(str(common.available_cores))
  cmd.append(ref_hmm)
  cmd.append(ref_msa)
  subprocess.check_call(cmd, cwd=out_dir)

  return os.path.join(out_dir, ref_hmm)


def launch_hmmalign(ref_hmm, ref_msa, query_fasta, out_dir):
  util.make_path(out_dir)

  out_file = "both.afa"

  cmd = []
  cmd.append( os.path.join(common.hmmer_dir, "hmmalign") )
  # if not util.is_slurm():
  #   cmd.append("--cpu")
  #   cmd.append(str(common.available_cores))
  cmd.append("-o")
  cmd.append(out_file)
  cmd.append("--outformat")
  cmd.append("afa")
  cmd.append("--mapali")
  cmd.append(ref_msa)
  cmd.append(ref_hmm)
  cmd.append(query_fasta)
  subprocess.check_call(cmd, cwd=out_dir)

  return os.path.join(out_dir, out_file)

