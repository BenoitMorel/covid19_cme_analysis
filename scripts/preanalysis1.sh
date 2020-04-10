input=$1
date=$2
alignment=$3

echo $date
echo $alignment

binpath=~/cov/bin/

$binpath/fasta2oneline.pl $input.fasta  > ${input}_oneline_${date}.fasta
$binpath/getFullSeq.pl -in  ${input}_oneline_${date}.fasta -length 29000 > ${input}_oneline_fullseq_${date}.fasta
$binpath/filterSequences.pl -in ${input}_oneline_fullseq_${date}.fasta > ${input}_oneline_fullseq_ns_${date}.fasta
if [[ "$alignment" != "" ]]; then
    $alignment ${input}_oneline_fullseq_ns_${date}.fasta > ${input}_oneline_fullseq_ns_${date}.aln
fi
