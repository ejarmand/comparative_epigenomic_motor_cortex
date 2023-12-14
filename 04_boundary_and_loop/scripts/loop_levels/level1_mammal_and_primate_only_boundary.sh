#!/bin/bash

module load bedtools

bedtools intersect -u -a ../liftover/human_union_boundary_hg38_with_rhemac10_element_rhemac10.bed -b ../../macaque/macaque_union_boundary.bed > human_boundary_with_macaque_boundary_any_celltypes_rhemac10.bed

bedtools intersect -u -a ../liftover/human_union_boundary_hg38_with_caljac4_element_caljac4.bed -b ../../marmoset/marmoset_union_boundary.bed > human_boundary_with_marmoset_boundary_any_celltypes_caljac4.bed

bedtools intersect -u -a ../liftover/human_union_boundary_hg38_with_mm10_element_mm10.bed -b ../../mouse/mouse_union_boundary.bed > human_boundary_with_mouse_boundary_any_celltypes_mm10.bed

cat human_boundary_with_*_boundary_any_celltypes_*.bed | cut -f4 | sort | uniq -c | grep ' 3 ' | sed 's/ 3 /3	/g' | cut -f2 | grep -Fw -f - ../liftover/human_union_boundary.bed > level1_mammal_boundary.bed

cat human_boundary_with_macaque_boundary_any_celltypes_rhemac10.bed human_boundary_with_marmoset_boundary_any_celltypes_caljac4.bed | cut -f4 | sort | uniq -c | grep ' 2 ' | sed 's/ 2 /2	/g' | cut -f2 | grep -Fw -f - ../liftover/human_union_boundary.bed > level1_primate_and_mammal_boundary.bed

cat level1_primate_and_mammal_boundary.bed level1_mammal_boundary.bed | sort | uniq -c | grep ' 1 ' | sed 's/ 1 /1	/g' | cut -f2-5 > level1_primate_only_boundary.bed
