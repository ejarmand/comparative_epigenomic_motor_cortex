jobstring = """#!/bin/bash
#PBS -q home-ren
#PBS -l nodes=1:ppn=4
#PBS -l walltime=8:00:00                                                                                             
#PBS -o /projects/ps-renlab2/earmand/projects/basenji/data/01_01_make_dataset_macaque.out
#PBS -e /projects/ps-renlab2/earmand/projects/basenji/data/01_01_make_dataset_macaque.er
#PBS -V
#PBS -N macaque_multiome_dataset                    
#PBS -m n

source ~/.bashrc

conda activate ~/miniconda3/envs/basenji
~/miniconda3/envs/basenji/bin/python /projects/ps-renlab2/earmand/projects/basenji/basenji/bin/basenji_data.py --local -l 131072 -p 16 -t 7,5,X -v 16,17,9 -w 128 -o /projects/ps-renlab2/earmand/projects/basenji/data/datasets/macaque_multiome /projects/ps-renlab2/earmand/projects/basenji/data/genomes/rhemac_no_chr.fa /projects/ps-renlab2/earmand/projects/basenji/data/datasets/macaque_with_paired_tag.tsv
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

cell_types_pt = ['ASC', 'CLAGL', 'CTGL', 'D12MSN', 'Exc', 'ITL23GL', 'ITL45GL',
       'ITL5GL', 'ITL6GL', 'Inh', 'MGL', 'NPGL', 'NonNeu', 'OBGA', 'OBGL',
       'OGC', 'OPC', 'PTGL', 'PVGA', 'SSTGA', 'STRGA', 'VIPGA', 'VLMC']

modifications = ['H3K27ac', 'H3K27me3']

specie = 'macaque'
lines = [['index','identifier','file','clip','sum_stat','description']]
count = 0
for cell_type in cell_types:
    line = [str(count), f'{cell_type}_{specie}_multiome_atac',
            f'/projects/ps-renlab2/earmand/projects/basenji/data/bw/{cell_type}_merge_{specie}_ATAC.bw',
            '384', 'sum', f'{specie}_{cell_type}']
    lines.append(line)
    count+=1

# for cell_type in cell_types_pt:
#     for mod in modifications:
#         line = [str(count), f'{specie}_{cell_type}_paired_tag_{mod}',
#                 f'/projects/ps-renlab2/earmand/projects/basenji/data/bw/dpt_merge_mouse_{cell_type}_{mod}_mod.bw',
#                 '384', 'sum', f'{specie}_{cell_type}_paired_tag_{mod}']
#         lines.append(line)
#         count +=1

samples_str = '/projects/ps-renlab2/earmand/projects/basenji/data/datasets/macaque_with_paired_tag.tsv'
        
samples_out = open(samples_str, 'w+')

for line in lines:
    print('\t'.join(line), file=samples_out)
samples_out.close()


species = ['human', 'macaque', 'marmoset', 'mouse']

name = '/projects/ps-renlab2/earmand/projects/basenji/jobs/macaque_dataset_w_paired_tag.job'

import os
open(name, 'w+' ).write(jobstring)
os.system('qsub ' + name)