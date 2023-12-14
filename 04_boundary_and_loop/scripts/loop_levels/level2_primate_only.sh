#!/bin/bash

module load bedtools

type=('Astro' 'CLA' 'L23' 'L4' 'L5-ET' 'L5-IT' 'L6b' 'L6-CT' 'L6-IT' 'Lamp5' 'MG' 'NP' 'ODC' 'OPC' 'Pvalb-BC' 'Pvalb-ChC' 'Sncg' 'Sst' 'Vip' 'Vsc')

for type in ${type[@]}

do

cat rhemac10_overlap/${type}_human_loop_overlap_rhemac10_${type}_loop_hg38.bedpe caljac4_overlap/${type}_human_loop_overlap_caljac4_${type}_loop_hg38.bedpe mm10_overlap/${type}_human_loop_overlap_mm10_${type}_loop_hg38.bedpe | cut -f7 | sort | uniq -c | grep ' 2 ' | sed 's/ 2 /2	/g' | cut -f2 | grep -Fw -f - ../level0/level0_primate_only_loops.bedpe > primate_only/${type}_human_loop_primate_only_level2.bedpe

done

cat primate_only/*_human_loop_primate_only_level2.bedpe | sort | uniq > primate_only/level2_primate_only_loops.bedpe
