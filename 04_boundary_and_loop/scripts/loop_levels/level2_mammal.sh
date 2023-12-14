#!/bin/bash

module load bedtools

type=('Astro' 'CLA' 'L23' 'L4' 'L5-ET' 'L5-IT' 'L6b' 'L6-CT' 'L6-IT' 'Lamp5' 'MG' 'NP' 'ODC' 'OPC' 'Pvalb-BC' 'Pvalb-ChC' 'Sncg' 'Sst' 'Vip' 'Vsc')

for type in ${type[@]}

do

cat rhemac10_overlap/${type}_human_boundary_overlap_rhemac10_${type}_boundary_hg38.bed caljac4_overlap/${type}_human_boundary_overlap_caljac4_${type}_boundary_hg38.bed mm10_overlap/${type}_human_boundary_overlap_mm10_${type}_boundary_hg38.bed | cut -f4 | sort | uniq -c | grep ' 3 ' | sed 's/ 3 /3	/g' | cut -f2 | grep -Fw -f - ../level0/level0_mammal_boundary.bed > mammal/${type}_human_boundary_mammal_level2.bed

done

cat mammal/*_human_boundary_mammal_level2.bed | sort | uniq > mammal/level2_mammal_boundary.bed
