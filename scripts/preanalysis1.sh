input=$1
date=$2
alignment=$3

BASE=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)

echo $date
echo $alignment

$BASE/fasta2oneline.pl $input.fasta  > ${input}_oneline_${date}.fasta
$BASE/getFullSeq.pl -in  ${input}_oneline_${date}.fasta -length 29000 > ${input}_oneline_fullseq_${date}.fasta
$BASE/filterSequences.pl -in ${input}_oneline_fullseq_${date}.fasta > ${input}_oneline_fullseq_ns_${date}.fasta
$BASE/remove_outgroup.pl -in ${input}_oneline_fullseq_ns_${date}.fasta -outgroup "BAT|PANGOLIN" > ${input}_oneline_fullseq_ns_NOTOUGROUP_${date}.fasta

if [[ "$alignment" != "" ]]; then
    $alignment ${input}_oneline_fullseq_ns_${date}.fasta > ${input}_oneline_fullseq_ns_${date}.aln
    $BASE/fasta2oneline.pl ${input}_oneline_fullseq_ns_${date}.aln > ${date}.aln
    $BASE/trimalignment.pl -in ${date}.aln -l 1000 > ${date}_trimmed.aln
    
    ## also the alignment for the dataset without the outgroup
    $alignment ${input}_oneline_fullseq_ns_NOOUTGROUP${date}.fasta > ${input}_oneline_fullseq_ns_NOOUTGROUP_${date}.aln
    $BASE/fasta2oneline.pl ${input}_oneline_fullseq_ns_${date}.aln > ${date}_nooutgroup.aln
    $BASE/trimalignment.pl -in ${date}_nooutgroup.aln -l 1000 > ${date}_nooutgroup_trimmed.aln
fi
