#!/bin/bash

#USAGE: bash liftover_reciprocal.sh input.bed starting_assembly conversion_assembly
#e.g. of chain file name: hg38Tomm10.over.chain.gz


liftOver -minMatch=0.5 $1 $2To$3.over.chain.gz $2_to_$3.bed $2_to_$3_unmapped.bed

awk '{ print $0 "\t" $3-$2}' $2_to_$3.bed | awk '(NR>1) && ($5 < 1001 ) ' | sort -n -k 5 > $2_to_$3_1kb_or_less.bed

liftOver -minMatch=0.5 $2_to_$3_1kb_or_less.bed $3To$2.over.chain.gz $2_to_$3_to_$2.bed $2_to_$3_to_$2_unmapped.bed

bedtools intersect -wo -a $1 -b $2_to_$3_to_$2.bed | awk '{if($4 == $8) print}' | cut -f1,2,3,4 > $2_with_$3_element.bed
