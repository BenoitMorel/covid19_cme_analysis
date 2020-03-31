import ete3
import os
import sys

def remove_duplicates(input_msa, output_msa):
  msa = ete3.SeqGroup(input_msa, format="fasta")
  new_msa = ete3.SeqGroup()
  duplicates = set()
  for entry in msa.iter_entries():
    if (entry[1] in duplicates):
      print(entry[0] + " is a duplicate")
      continue
    duplicates.add(entry[1])
    new_msa.set_seq(entry[0], entry[1])
  
  print("Found " + str(len(msa) - len(new_msa)) + " duplicates")
  new_msa.write("fasta", output_msa)
  print("New msa writen in " + output_msa)
  print("msa length: " + str(len(new_msa)))


if (__name__ == "__main__"):
  if (len(sys.argv) != 3):
    print("Syntax: input_msa output_msa")
    sys.exit(1)
  input_msa = sys.argv[1]
  output_msa = sys.argv[2]
  remove_duplicates(input_msa, output_msa)

