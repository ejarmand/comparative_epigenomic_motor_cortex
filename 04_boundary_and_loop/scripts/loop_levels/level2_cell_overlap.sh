#!/bin/bash

module load bedtools

type=('Astro' 'CLA' 'L23' 'L4' 'L5-ET' 'L5-IT' 'L6b' 'L6-CT' 'L6-IT' 'Lamp5' 'MG' 'NP' 'ODC' 'OPC' 'Pvalb-BC' 'Pvalb-ChC' 'Sncg' 'Sst' 'Vip' 'Vsc')

for type in ${type[@]}

do

bedtools intersect -u -a ../liftover/rhemac10/celltype/${type}_with_rhemac10_element_rhemac10.bed -b ../../macaque/${type}_from_union_boundary.bed > rhemac10_overlap/${type}_human_boundary_overlap_rhemac10_${type}_boundary_rhemac10.bed

bedtools intersect -u -a ../liftover/caljac4/celltype/${type}_with_caljac4_element_caljac4.bed -b ../../marmoset/${type}_from_union_boundary.bed > caljac4_overlap/${type}_human_boundary_overlap_caljac4_${type}_boundary_caljac4.bed

bedtools intersect -u -a ../liftover/mm10/celltype/${type}_with_mm10_element_mm10.bed -b ../../mouse/${type}_from_union_boundary.bed  > mm10_overlap/${type}_human_boundary_overlap_mm10_${type}_boundary_mm10.bed

bedtools intersect -u -a ../liftover/rhemac10/celltype/${type}_with_rhemac10_element_rhemac10.bed -b ../../macaque/${type}_from_union_boundary.bed | cut -f4 | grep -Fw -f - ../liftover/human_union_boundary_hg38_with_rhemac10_element.bed > rhemac10_overlap/${type}_human_boundary_overlap_rhemac10_${type}_boundary_hg38.bed

bedtools intersect -u -a ../liftover/caljac4/celltype/${type}_with_caljac4_element_caljac4.bed -b ../../marmoset/${type}_from_union_boundary.bed | cut -f4 | grep -Fw -f - ../liftover/human_union_boundary_hg38_with_caljac4_element.bed > caljac4_overlap/${type}_human_boundary_overlap_caljac4_${type}_boundary_hg38.bed

bedtools intersect -u -a ../liftover/mm10/celltype/${type}_with_mm10_element_mm10.bed -b ../../mouse/${type}_from_union_boundary.bed | cut -f4 | grep -Fw -f - ../liftover/human_union_boundary_hg38_with_mm10_element.bed > mm10_overlap/${type}_human_boundary_overlap_mm10_${type}_boundary_hg38.bed

done
