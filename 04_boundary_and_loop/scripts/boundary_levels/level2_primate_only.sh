#!/bin/bash

module load bedtools

type=('Astro' 'CLA' 'L23' 'L4' 'L5-ET' 'L5-IT' 'L6b' 'L6-CT' 'L6-IT' 'Lamp5' 'MG' 'NP' 'ODC' 'OPC' 'Pvalb-BC' 'Pvalb-ChC' 'Sncg' 'Sst' 'Vip' 'Vsc')

for type in ${type[@]}

do

cat rhemac10_overlap/${type}_human_boundary_overlap_rhemac10_${type}_boundary_hg38.bed caljac4_overlap/${type}_human_boundary_overlap_caljac4_${type}_boundary_hg38.bed mm10_overlap/${type}_human_boundary_overlap_mm10_${type}_boundary_hg38.bed | cut -f4 | sort | uniq -c | grep ' 2 ' | sed 's/ 2 /2	/g' | cut -f2 | grep -Fw -f - ../level0/level0_primate_only_boundary.bed > primate_only/${type}_human_boundary_primate_only_level2.bed

done

cat primate_only/*_human_boundary_primate_only_level2.bed | sort | uniq > primate_only/level2_primate_only_boundary.bed
