#!/bin/bash
# USAGE
# three arguments
# path to bedgraphs
# path to peak file
# path to outdir

bedtools="/home/earmand/conda_envs/bedtools/bin/bedtools"

mkdir -p $3
ls $1 | grep "bedgraph" | while read -r line; do
    bedtools intersect -wa -wb -a $2 -b ${1}/$line > ${3}/$line;
done