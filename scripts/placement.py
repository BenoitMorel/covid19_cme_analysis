import os
import sys
import launcher
import common
import subprocess as sub
import util
from glob import glob

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
  sub.check_call(cmd, cwd=out_dir)

  return os.path.join(out_dir, new_ref_msa), os.path.join(out_dir, query_msa)

def outgroup_check(jplace_files, out_dir):
  for f in jplace_files:
    util.expect_file_exists( f )
  util.make_path( out_dir )

  cmd = []
  cmd.append(common.genesis_outgroup_check)
  for f in jplace_files:
    cmd.append(f)

  outfile = os.path.join( out_dir, "outgroup_check.txt" )
  with open( outfile, "w+" ) as logfile:
    sub.check_call(cmd, stdout=logfile)

  return outfile

def gappa_examine_lwr(jplace_path, out_dir):
  util.make_path( out_dir )

  # gappa examine lwr --jplace-path ./*/*.jplace --no-list-file --out-dir ../../results/epa_rooting/
  cmd = []
  cmd.append(common.gappa)
  cmd.append("examine")
  cmd.append("lwr")
  cmd.append("--jplace-path")
  cmd += glob(jplace_path)
  cmd.append("--no-list-file")
  cmd.append("--no-compat-check")
  cmd.append("--allow-file-overwriting")
  cmd.append("--histogram-bins")
  cmd.append("20")
  cmd.append("--out-dir")
  cmd.append(out_dir)
  sub.check_call(cmd)

  return os.path.join( out_dir, "lwr_histogram.csv" )

def ggplot_lwr_histogram(hist_csv_file, out_dir):
  util.make_path( out_dir )

  # gappa examine lwr --jplace-path ./*/*.jplace --no-list-file --out-dir ../../results/epa_rooting/
  cmd = []
  cmd.append( os.path.join(common.scripts_dir, "lwr_hist.r") )
  cmd.append(hist_csv_file)
  # get the input file name without ending
  f_name=os.path.splitext( os.path.basename(hist_csv_file) )[0]
  out_file=os.path.join(out_dir, f_name+".pdf")
  cmd.append(out_file)
  sub.check_call(cmd)

  return out_file

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
  sub.check_call(cmd, stdout=sub.DEVNULL)

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
  sub.check_call(cmd)

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
  sub.check_call(cmd, cwd=out_dir)

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
  sub.check_call(cmd, cwd=out_dir)

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
  sub.check_call(cmd, cwd=out_dir)

  return os.path.join(out_dir, out_file)

