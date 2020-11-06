#!/bin/bash

# Run this first on the basis input sequences:
#grep ">" gisaid_hcov-19_2020_05_05_19.fasta | cut -f 2 -d"/" | sort | uniq -c | sed "s/ \([A-Z].*\) \([A-Z].*\)/ \1\2/g" > refcounts.txt
# --> and then remove one last remaining space from UAE... too lazy to also code that

mkdir -p counts
outfile="final.txt"
echo -ne "country\tinput" > $outfile

# count all fasta files individually
for f in `ls *.fa`; do
	#echo $f
	#grep ">" $f | wc -l
	
	# count occurrences of country names in the input file
	grep ">" $f | cut -f 2 -d"_" | sort | uniq -c > counts/${f}.counts
	
	# write a column header for the final out file
	echo -ne "\t${f%.fa}" >> $outfile
done
echo >> $outfile

# and combine them into one table, sorted by the reference.
# we go through the counts of the reference (basis input sequence file),
# which is a list of counts per country, and then find these country entries
# in each of the indivudal fasta count files that we produced above.
# then, we put all these counts into one line for the output
input="counts/refcounts.txt"
while IFS= read -r line
do
	# get the country name and its count of occurrences in the reference file
	cnt=`echo "$line"  | tr -s ' ' | cut -f 2 -d" "`
	name=`echo "$line" | tr -s ' ' | cut -f 3 -d" "`
	
	# print it
	echo "$name --> $cnt"
	echo -ne "$name\t$cnt" >> $outfile
	
	# now go through all fasta files of our alignments, find that country, 
	# and print its count of occurrences in that fasta file to our output
	for f in `ls *.fa`; do
		fcnt=`egrep -i " $name$" counts/${f}.counts | tr -s " " | cut -f 2 -d" "`
		if [ -z "$fcnt" ]; then
			fcnt="0"
		fi
		echo -ne "\t$fcnt" >> $outfile
	done
	echo >> $outfile
done < "$input"
