#!/bin/bash

module load bedtools

type=('Astro' 'CLA' 'L23' 'L4' 'L5-ET' 'L5-IT' 'L6b' 'L6-CT' 'L6-IT' 'Lamp5' 'MG' 'NP' 'ODC' 'OPC' 'Pvalb-BC' 'Pvalb-ChC' 'Sncg' 'Sst' 'Vip' 'Vsc')

for type in ${type[@]}

do

cat rhemac10_overlap/${type}_human_loop_overlap_rhemac10_${type}_loop_hg38.bedpe caljac4_overlap/${type}_human_loop_overlap_caljac4_${type}_loop_hg38.bedpe mm10_overlap/${type}_human_loop_overlap_mm10_${type}_loop_hg38.bedpe | cut -f7 | sort | uniq -c | grep ' 3 ' | sed 's/ 3 /3	/g' | cut -f2 | grep -Fw -f - ../level0/level0_mammal_loops.bedpe > mammal/${type}_human_loop_mammal_level2.bedpe

done

cat mammal/*_human_loop_mammal_level2.bedpe | sort | uniq > mammal/level2_mammal_loops.bedpe
