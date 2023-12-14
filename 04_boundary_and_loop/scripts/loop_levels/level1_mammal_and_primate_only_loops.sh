#!/bin/bash

module load bedtools

pairToPair -type both -a ../liftover/union_loop_summit_hg38_with_rhemac10_element_rhemac10.bedpe -b ../../macaque/union_loop_summit.bedpe | cut -f1-7 | sort | uniq > human_loop_with_macaque_loop_any_celltypes_rhemac10.bedpe

pairToPair -type both -a ../liftover/union_loop_summit_hg38_with_caljac4_element_caljac4.bedpe -b ../../marmoset/union_loop_summit.bedpe | cut -f1-7 | sort | uniq > human_loop_with_marmoset_loop_any_celltypes_caljac4.bedpe

pairToPair -type both -a ../liftover/union_loop_summit_hg38_with_mm10_element_mm10.bedpe -b ../../mouse/union_loop_summit.bedpe | cut -f1-7 | sort | uniq > human_loop_with_mouse_loop_any_celltypes_mm10.bedpe

cat human_loop_with*_loop_any_celltypes_*.bedpe | cut -f7 | sort | uniq -c | grep ' 3 ' | sed 's/ 3 /3	/g' | cut -f2 | grep -Fw -f - ../liftover/union_loop_summit.bedpe > level1_mammal_loops.bedpe

cat human_loop_with_macaque_loop_any_celltypes_rhemac10.bedpe human_loop_with_marmoset_loop_any_celltypes_caljac4.bedpe | cut -f7 | sort | uniq -c | grep ' 2 ' | sed 's/ 2 /2	/g' | cut -f2 | grep -Fw -f - ../liftover/union_loop_summit.bedpe > level1_primate_and_mammal_loops.bedpe

cat level1_primate_and_mammal_loops.bedpe level1_mammal_loops.bedpe | sort | uniq -c | grep ' 1 ' | sed 's/ 1 /1	/g' | cut -f2-8 > level1_primate_only_loops.bedpe
