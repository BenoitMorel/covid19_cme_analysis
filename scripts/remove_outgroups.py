import ete3
import os
import sys

def remove_outgroups(input_msa, output_msa, outgroups):
  msa = ete3.SeqGroup(input_msa, format="fasta")
  new_msa = ete3.SeqGroup()
  duplicates = set()
  for entry in msa.iter_entries():
    for outgroup in outgroups:
      if (outgroup in entry[0]):
        print("Removing outgroup " + entry[0])
        continue
    new_msa.set_seq(entry[0], entry[1])
  
  new_msa.write("fasta", output_msa)
  print("msa length: " + str(len(new_msa)))
  print("New msa writen in " + output_msa)



