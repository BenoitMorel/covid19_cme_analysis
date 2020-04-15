#!/bin/bash

input=$1
date=$2
scriptdir=$3
alignment=$4
cores=$5

file="${input%%.*}"
name="${file##*/}"

echo $scriptdir
echo $name
echo $date
echo $alignment

set -e

${scriptdir}/fasta2oneline.pl $input  > ${name}_oneline_${date}.fasta
${scriptdir}/getFullSeq.pl -in  ${name}_oneline_${date}.fasta -length 29000 > ${name}_oneline_fullseq_${date}.fasta
${scriptdir}/filterSequences.pl -in ${name}_oneline_fullseq_${date}.fasta > ${name}_oneline_fullseq_ns_${date}.fasta
${scriptdir}/remove_outgroup.pl -in ${name}_oneline_fullseq_ns_${date}.fasta -outgroup "BAT|PANGOLIN" > ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.fasta

if [[ "$alignment" != "" ]]; then
    # $alignment --thread $cores ${name}_oneline_fullseq_ns_${date}.fasta > ${name}_oneline_fullseq_ns_${date}.aln
    # ${scriptdir}/fasta2oneline.pl ${name}_oneline_fullseq_ns_${date}.aln > ${date}.aln
    # ${scriptdir}/trimalignment.pl -in ${date}.aln -l 1000 > ${date}_trimmed.aln
    
    ## also the alignment for the dataset without the outgroup
    $alignment --thread $cores ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.fasta > ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.aln
    ${scriptdir}/fasta2oneline.pl ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.aln > ${date}_nooutgroup.aln
    ${scriptdir}/trimalignment.pl -in ${date}_nooutgroup.aln -l 1000 > ${date}_nooutgroup_trimmed.aln
fi
