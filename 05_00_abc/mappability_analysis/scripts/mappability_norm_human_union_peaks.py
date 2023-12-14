import os
import pandas as pd

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
 'VLMC'
             ]


bwavg = '/projects/ps-renlab2/earmand/conda_envs/bigwigtools/bin/bigWigAverageOverBed'
map_score = '../hg38/k100_map_score.bw'

# remove peaks below min map
min_map = .1 

ref_file = '/home/nzemke/renlab2/multiome/mop_m1_integration/human_atac/raw_atac_counts/human_union_atac_counts.tsv'

abc_ref = pd.read_csv(ref_file, sep='\t')


peak_bed = f'/projects/ps-renlab2/earmand/projects/mammalian_motor_cortex_comparative/mappability/mappability_intermediate_data/human_union_peaks.bed'

peak_out_cmd = f'cat {ref_file} | cut -f 1 | cut -s -d"-" --output-delimiter $"\t" -f1,2,3 > peak_bed_tpm.bed'
os.system(peak_out_cmd)


os.system(f'cut -f1 {ref_file} | tail -n +2  > peak_names_tmp.txt')

paste_cmd = f'paste peak_bed_tpm.bed peak_names_tmp.txt > {peak_bed}'
os.system(paste_cmd)
print(paste_cmd)

# abc_ref[['chr', 'start', 'end', 'peak']].to_csv(peak_bed,
#                header=None, index=None, sep='\t')

map_quant_out = f'../mappability_intermediate_data/union_atac_mappability.txt'
mapability_command = f'{bwavg} {map_score} {peak_bed} {map_quant_out}'
print(mapability_command)
os.system(mapability_command)

map_quant = pd.read_csv(map_quant_out, sep='\t', header=None).set_index(0)

abc_ref = abc_ref.set_index('peak')
abc_ref = abc_ref.join(map_quant[4].rename('mappability'))

# threshold on mapability

abc_ref = abc_ref.loc[abc_ref.mappability > .1]

norm_counts_cols = (abc_ref[cell_types].T/abc_ref['mappability']).T

norm_counts_cols['mappability'] = abc_ref['mappability']
# norm_counts_cols[['chr', 'start', 'end', 'peak']] = abc_ref.reset_index()[['chr', 'start', 'end', 'peak']]

norm_counts_cols['peak'] = abc_ref.reset_index()[ 'peak']

norm_counts_cols = norm_counts_cols[['peak', 'mappability'] + cell_types]

norm_counts_cols.to_csv('/projects/ps-renlab2/earmand/for_others/nathan/mammalian_motor_cortex_comparative/mapability/atac_500bp_human_all_peaks_mappability_norm.tsv', sep='\t')
                    
