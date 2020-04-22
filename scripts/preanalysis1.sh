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

remove_outgroup=${scriptdir}/../software/genesis/bin/apps/remove_sequences

set -e

${scriptdir}/fasta2oneline.pl $input  > ${name}_oneline_${date}.fasta
${scriptdir}/getFullSeq.pl -in  ${name}_oneline_${date}.fasta -length 29000 > ${name}_oneline_fullseq_${date}.fasta
${scriptdir}/filterSequences.pl -in ${name}_oneline_fullseq_${date}.fasta > ${name}_oneline_fullseq_ns_${date}.fasta
# ${scriptdir}/remove_outgroup.pl -in ${name}_oneline_fullseq_ns_${date}.fasta -outgroup "BAT|PANGOLIN" > ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.fasta
${remove_outgroup} ${name}_oneline_fullseq_ns_${date}.fasta ${scriptdir}/../config/outgroups.txt ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.fasta covid_outgroups_untrimmed.fasta

if [[ "$alignment" != "" ]]; then
    # $alignment --thread $cores ${name}_oneline_fullseq_ns_${date}.fasta > ${name}_oneline_fullseq_ns_${date}.aln
    # ${scriptdir}/fasta2oneline.pl ${name}_oneline_fullseq_ns_${date}.aln > ${date}.aln
    # ${scriptdir}/trimalignment.pl -in ${date}.aln -l 1000 > ${date}_trimmed.aln

    ## also the alignment for the dataset without the outgroup
	echo $alignment
    $alignment --thread $cores ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.fasta > ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.aln
    ${scriptdir}/fasta2oneline.pl ${name}_oneline_fullseq_ns_NOOUTGROUP_${date}.aln > ${date}_nooutgroup.aln
    ${scriptdir}/trimalignment.pl -in ${date}_nooutgroup.aln -l 1000 > ${date}_nooutgroup_trimmed.aln
    # singleton removal
    ${scriptdir}/removekclass.pl -in ${date}_nooutgroup_trimmed.aln -k 1 > ${date}_nooutgroup_trimmed_nosingle.aln

    ${scriptdir}/fasta2oneline.pl covid_outgroups_untrimmed.fasta >  covid_outgroups_untrimmed_oneline.fasta
    ${scriptdir}/trimalignment.pl -in covid_outgroups_untrimmed_oneline.fasta -l 1000 > covid_outgroups.fasta
fi
