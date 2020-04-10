BASE=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)

input=$1
date=$2
alignment=$3

echo $date
echo $alignment

${BASE}/fasta2oneline.pl $input.fasta  > ${input}_oneline_${date}.fasta
${BASE}/getFullSeq.pl -in  ${input}_oneline_${date}.fasta -length 29000 > ${input}_oneline_fullseq_${date}.fasta
${BASE}/filterSequences.pl -in ${input}_oneline_fullseq_${date}.fasta > ${input}_oneline_fullseq_ns_${date}.fasta
if [[ "$alignment" != "" ]]; then
    $alignment ${input}_oneline_fullseq_ns_${date}.fasta > ${input}_oneline_fullseq_ns_${date}.aln
fi
