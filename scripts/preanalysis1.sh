#!/bin/bash

input=$1
mode=$2
scriptdir=$3
alignment=$4
outgroups_to_remove=$5
version_dir=$6
cores=$7

remove_sequences=${scriptdir}/../software/genesis/bin/apps/remove_sequences

file="${input%%.*}"
name="${file##*/}"

# "fmsao", "fmsan", "smsao", "smsan"
case "$mode" in
  fmsao )
    include_outgroups=1
    include_singletons=1
    other_mode=smsao
    ;;
  fmsan )
    include_outgroups=0
    include_singletons=1
    other_mode=smsan
    ;;
  smsao )
    include_outgroups=1
    include_singletons=0
    other_mode=fmsao
    ;;
  smsan )
    include_outgroups=0
    include_singletons=0
    other_mode=fmsan
    ;;
  *)
    echo "invalid mode (${mode}), aborting"
    exit 1
esac

set -e


# first, check if we already have an alignment we can copy
other_runs_dir=${version_dir}/${other_mode}/runs/preanalysis_runs
if [[ ${include_singletons} -eq 1 ]]; then
    # if we want the alignment with singletons, check if the respective smsa* exists,
    if [[ -f ${other_runs_dir}/preprocessed_with_single.fasta ]]; then
        echo "Found previous alignment results at ${other_runs_dir}, copying over and switching to singleton-included MSA"
        # copy everything over,
        cp ${other_runs_dir}/* .
        # and rename preprocessed_with_single.fasta to preprocessed.fasta
        mv preprocessed_with_single.fasta preprocessed.fasta

        # and done! exit!
        exit 0
    fi
else
    # if we want it without singletons, check if the respective fmsa* exists,
    if [[ -f ${other_runs_dir}/preprocessed.fasta ]]; then
        echo "Found previous alignment results at ${other_runs_dir}, copying over and applying singleton removal"
        # copy everything over,
        cp ${other_runs_dir}/* .
        # and apply singleton removal as usual
        ${scriptdir}/removekclass.pl -in preprocessed.fasta -k 1 > tmp.fasta
        mv preprocessed.fasta preprocessed_with_single.fasta
        mv tmp.aln preprocessed.fasta

        # and done! exit!
        exit 0
    fi
fi

# elsewise, do the whole dance

${scriptdir}/fasta2oneline.pl $input  > ${name}_oneline.fasta
${scriptdir}/getFullSeq.pl -in  ${name}_oneline.fasta -length 29000 > ${name}_oneline_fullseq.fasta
${scriptdir}/filterSequences.pl -in ${name}_oneline_fullseq.fasta > ${name}_oneline_fullseq_ns.fasta

if [[ ${include_outgroups} -eq 0 ]]; then
    # outgroups_to_remove=/dev/null
    ${remove_sequences} ${name}_oneline_fullseq_ns.fasta ${outgroups_to_remove} ${name}_oneline_fullseq_ns_tmp.fasta covid_outgroups_untrimmed.fasta
    mv ${name}_oneline_fullseq_ns_tmp.fasta ${name}_oneline_fullseq_ns.fasta
    ${scriptdir}/fasta2oneline.pl covid_outgroups_untrimmed.fasta >  covid_outgroups_untrimmed_oneline.fasta
    ${scriptdir}/trimalignment.pl -in covid_outgroups_untrimmed_oneline.fasta -l 1000 > covid_outgroups.fasta
fi

$alignment --thread $cores ${name}_oneline_fullseq_ns.fasta > ${name}_oneline_fullseq_ns.aln
${scriptdir}/fasta2oneline.pl ${name}_oneline_fullseq_ns.aln > ${name}_oneline_fullseq_ns_oneline.aln
${scriptdir}/trimalignment.pl -in _oneline_fullseq_ns_oneline.aln -l 1000 > preprocessed.fasta

if [[ ${include_singletons} -eq 0 ]]; then
    # singleton removal
    ${scriptdir}/removekclass.pl -in preprocessed.fasta -k 1 > tmp.fasta
    mv preprocessed.fasta preprocessed_with_single.fasta
    mv tmp.aln preprocessed.fasta
fi
