#!/bin/bash

dir="/ATAC_bam/"

type=('ASC' 'ChC' 'Endo' 'L2_3_IT' 'L4_5_IT' 'L5_6_NP' 'L5_ET' 'L5_IT' 'L6b' 'L6_CT' 'L6_IT' 'L6_IT_CAR3' 'LAMP5' 'MGC' 'OGC' 'OPC' 'PVALB' 'SNCG' 'SST' 'VIP' 'VLMC')

for type in ${type[@]}

do

mkdir ${type}

macs2 callpeak --treatment ${dir}${type}_merge_human_ATAC.bam --shift -75 --ext 150 -g hs --name ${type} --bdg -q 0.1 -B --SPMR --call-summits -f BAMPE

done
