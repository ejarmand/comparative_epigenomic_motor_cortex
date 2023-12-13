jobstring = """#!/bin/bash
#PBS -q condo
#PBS -l nodes=1:ppn=4
#PBS -l walltime=8:00:00                                                                                             
#PBS -o /projects/ps-renlab2/earmand/projects/basenji/data/03_marmoset_mcg_atac.out
#PBS -e /projects/ps-renlab2/earmand/projects/basenji/data/03_marmoset_mcg_atac.er
#PBS -V
#PBS -N marmoset_dnn_both                     
#PBS -m n

source ~/.bashrc


conda activate ~/miniconda3/envs/basenji
python /projects/ps-renlab2/earmand/projects/basenji/basenji/bin/basenji_data.py --local -l 131072 -p 16 -t chr10,chr3,chrX -v chr5,chr12 -w 128 -o /projects/ps-renlab2/earmand/projects/basenji/data/datasets/marmoset_mcg_atac /projects/ps-renlab2/earmand/projects/basenji/data/genomes/calJac4.fa /projects/ps-renlab2/earmand/projects/basenji/data/datasets/marmoset_mcg_atac.tsv

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
 # 'VLMC'
             ]


specie = 'marmoset'
lines = [['index','identifier','file','clip','sum_stat','description']]
count = 0
for cell_type in cell_types:
    line = [str(count), f'{cell_type}_{specie}_mcg',
            f'/projects/ps-renlab2/earmand/projects/basenji/data/mcg_bw/{specie}/{cell_type}.CGN-both.bw',
            '384', 'mean', f'{specie}_{cell_type}']
    lines.append(line)
    count+=1



for cell_type in cell_types:
    line = [str(count), f'{cell_type}_{specie}_multiome_atac',
            f'/projects/ps-renlab2/earmand/projects/basenji/data/bw/{cell_type}_merge_{specie}_ATAC.bw',
            '384', 'sum', f'{specie}_{cell_type}']
    lines.append(line)
    count+=1

samples_str = '/projects/ps-renlab2/earmand/projects/basenji/data/datasets/marmoset_mcg_atac.tsv'
        
samples_out = open(samples_str, 'w+')

for line in lines:
    print('\t'.join(line), file=samples_out)
samples_out.close()


name = '/projects/ps-renlab2/earmand/projects/basenji/jobs/marmoset_mcg_atac.job'

import os
open(name, 'w+' ).write(jobstring)
os.system('qsub ' + name)
