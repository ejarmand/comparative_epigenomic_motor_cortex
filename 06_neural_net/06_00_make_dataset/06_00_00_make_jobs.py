jobstring = """#!/bin/bash
#PBS -q condo
#PBS -l nodes=1:ppn=16
#PBS -l mem=250gb                                                                                                       
#PBS -l walltime=8:00:00                                                                                             
#PBS -o /projects/ps-renlab2/earmand/projects/basenji/data/{0}_{1}.out
#PBS -e /projects/ps-renlab2/earmand/projects/basenji/data/{0}_{1}.er
#PBS -V
#PBS -N dnn_dataset                        
#PBS -m n

~/miniconda3/envs/basenji/bin/python \
/projects/ps-renlab2/earmand/projects/basenji/basenji/bin/bam_cov.py /projects/ps-renlab2/earmand/projects/basenji/data/bams/{0}/{1}_merge_{0}_ATAC.bam /projects/ps-renlab2/earmand/projects/basenji/data/bw/{1}_merge_{0}_ATAC.bw"""

cell_types = ['ASC',
 'ChC',
 'Endo',
 'L2_3_IT',
 'L4_5_IT',
 'L5_6_NP',
 'L5_ET',
 'L5_IT',
 'L6b',
 'L6_CT',
 'L6_IT_CAR3',
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

species = ['human', 'macaque', 'marmoset', 'mouse']

name = '/projects/ps-renlab2/earmand/projects/basenji/jobs/{0}_{1}_coverage.job'

import os

for specie in species:
    for ct in cell_types:
        open(name.format(specie, ct), 'w+' ).write(jobstring.format(specie, ct))
        if specie == 'macaque':
            os.system('qsub ' + name.format(specie, ct))