jobstring = """#!/bin/bash
#PBS -q condo
#PBS -l nodes=1:ppn=4
#PBS -l walltime=8:00:00                                                                                             
#PBS -o /projects/ps-renlab2/earmand/projects/basenji/data/01_00_make_dataset_mouse.out
#PBS -e /projects/ps-renlab2/earmand/projects/basenji/data/01_00_make_dataset_mouse.er
#PBS -V
#PBS -N dnn_dataset                        
#PBS -m n

source ~/.bashrc


conda activate ~/miniconda3/envs/basenji
~/miniconda3/envs/basenji/bin/python /projects/ps-renlab2/earmand/projects/basenji/basenji/bin/basenji_data.py --local -l 131072 -p 16 -t chr12,chr5,chrX -v chr19,chr14,chr11 -w 128 -o /projects/ps-renlab2/earmand/projects/basenji/data/datasets/mouse_w_paired_tag /projects/ps-renlab2/earmand/projects/basenji/data/genomes/mm10.fa /projects/ps-renlab2/earmand/projects/basenji/data/datasets/mouse_with_paired_tag.tsv

~/miniconda3/envs/basenji/bin/python /projects/ps-renlab2/earmand/projects/basenji/basenji/bin/basenji_data.py --local -l 131072 -p 16 -t chr12,chr5,chrX -v chr19,chr14,chr11 -w 128 -o /projects/ps-renlab2/earmand/projects/basenji/data/datasets/mouse_multiome /projects/ps-renlab2/earmand/projects/basenji/data/genomes/mm10.fa /projects/ps-renlab2/earmand/projects/basenji/data/datasets/mouse_multiome.tsv


"""

cell_types = ['ASC',
 # 'ChC',
 # 'Endo',
 'L2_3_IT',
 'L4_5_IT',
 'L5_6_NP',
 # 'L5_ET',
 'L5_IT',
 'L6b',
 'L6_CT',
 # 'L6_IT_CAR3',
 'L6_IT',
 'LAMP5',
 'MGC',
 'ODC',
 'OPC',
 'PVALB',
 'SNCG',
 'SST',
 'VIP',
 'VLMC']

count = 0
for cell_type in cell_types:
    line = [str(count), f'{cell_type}_{specie}_multiome_atac',
            f'/projects/ps-renlab2/earmand/projects/basenji/data/bw/{cell_type}_merge_{specie}_ATAC.bw',
            '384', 'sum', f'{specie}_{cell_type}']
    lines.append(line)
    count+=1

samples_str = '/projects/ps-renlab2/earmand/projects/basenji/data/datasets/mouse_multiome.tsv'
        
samples_out = open(samples_str, 'w+')

for line in lines:
    print('\t'.join(line), file=samples_out)


name = '/projects/ps-renlab2/earmand/projects/basenji/jobs/mouse_multiome.job'

import os
open(name, 'w+' ).write(jobstring)
os.system('qsub ' + name)
