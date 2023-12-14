#!/bin/bash

module load bedtools

type=('Astro' 'CLA' 'L23' 'L4' 'L5-ET' 'L5-IT' 'L6b' 'L6-CT' 'L6-IT' 'Lamp5' 'MG' 'NP' 'ODC' 'OPC' 'Pvalb-BC' 'Pvalb-ChC' 'Sncg' 'Sst' 'Vip' 'Vsc')

for type in ${type[@]}

do

pairToPair -type both -a ../liftover/rhemac10/celltype/${type}_with_rhemac10_element_rhemac10.bedpe -b ../../macaque/${type}_from_union_loop_summit.bedpe | cut -f1-7 > rhemac10_overlap/${type}_human_loop_overlap_rhemac10_${type}_loop_rhemac10.bedpe

pairToPair -type both -a ../liftover/caljac4/celltype/${type}_with_caljac4_element_caljac4.bedpe -b ../../marmoset/${type}.loop_summit.bedpe | cut -f1-7 > caljac4_overlap/${type}_human_loop_overlap_caljac4_${type}_loop_caljac4.bedpe

pairToPair -type both -a ../liftover/mm10/celltype/${type}_with_mm10_element_mm10.bedpe -b ../../mouse/${type}.loop_summit.bedpe | cut -f1-7 > mm10_overlap/${type}_human_loop_overlap_mm10_${type}_loop_mm10.bedpe

pairToPair -type both -a ../liftover/rhemac10/celltype/${type}_with_rhemac10_element_rhemac10.bedpe -b ../../macaque/${type}_from_union_loop_summit.bedpe | cut -f7 | grep -Fw -f - ../liftover/union_loop_summit_hg38_with_rhemac10_element.bedpe > rhemac10_overlap/${type}_human_loop_overlap_rhemac10_${type}_loop_hg38.bedpe

pairToPair -type both -a ../liftover/caljac4/celltype/${type}_with_caljac4_element_caljac4.bedpe -b ../../marmoset/${type}.loop_summit.bedpe | cut -f7 | grep -Fw -f - ../liftover/union_loop_summit_hg38_with_caljac4_element.bedpe > caljac4_overlap/${type}_human_loop_overlap_caljac4_${type}_loop_hg38.bedpe

pairToPair -type both -a ../liftover/mm10/celltype/${type}_with_mm10_element_mm10.bedpe -b ../../mouse/${type}.loop_summit.bedpe | cut -f7 | grep -Fw -f - ../liftover/union_loop_summit_hg38_with_mm10_element.bedpe > mm10_overlap/${type}_human_loop_overlap_mm10_${type}_loop_hg38.bedpe


done
