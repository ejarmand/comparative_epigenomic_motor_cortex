import os
import pandas as pd

cell_types = ['ASC',
 'ChC',
 # 'Endo',
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
 # 'VLMC'
             ]


bwavg = '/projects/ps-renlab2/earmand/conda_envs/bigwigtools/bin/bigWigAverageOverBed'
map_score = '../hg38/k100_map_score.bw'

# remove peaks below min map
min_map = .1 

ref_file = '/home/nzemke/renlab2/multiome/mop_m1_integration/human_atac/droplet_paired_tag_counts/h3k27ac_counts/human_union_human_m1_atac_union_4kb_dpt_h3k27ac_counts.tsv'

abc_ref = pd.read_csv(ref_file, sep='\t')


peak_bed = f'../mappability_intermediate_data/k3k27ac_peaks.bed'
abc_ref[['chr', 'start', 'end', 'peak']].to_csv(peak_bed,
               header=None, index=None, sep='\t')

map_quant_out = f'../mappability_intermediate_data/h3k27ac_mappability.txt'
mapability_command = f'{bwavg} {map_score} {peak_bed} {map_quant_out}'
os.system(mapability_command)

map_quant = pd.read_csv(map_quant_out, sep='\t', header=None).set_index(0)
abc_ref = abc_ref.set_index('peak')
abc_ref = abc_ref.join(map_quant[4].rename('mappability'))

# threshold on mapability

abc_ref = abc_ref.loc[abc_ref.mappability > .1]

norm_counts_cols = (abc_ref[cell_types].T/abc_ref['mappability']).T

norm_counts_cols['mappability'] = abc_ref['mappability']
norm_counts_cols[['chr', 'start', 'end', 'peak']] = abc_ref.reset_index()[['chr', 'start', 'end', 'peak']]

norm_counts_cols = norm_counts_cols[['chr', 'start', 'end', 'peak', 'mappability'] + cell_types]

norm_counts_cols.to_csv('/projects/ps-renlab2/earmand/for_others/nathan/mammalian_motor_cortex_comparative/mapability/k27ac_4kb_human_level0_mappability_norm.tsv', sep='\t')
                    
