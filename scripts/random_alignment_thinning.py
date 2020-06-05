import sys
import os
import ete3
import random

def thin(input_ali, output_ali, seq_number):
  input_msa = ete3.SeqGroup(input_ali)
  output_msa = ete3.SeqGroup()
  entries = input_msa.get_entries()
  random.shuffle(entries)
  for entry in entries[:seq_number]:
    output_msa.set_seq(entry[0], entry[1])
  output_msa.write(outfile = output_ali)
  print("Writing randomly thinned alignment with " + str(seq_number) + " sequences into " + output_ali)

