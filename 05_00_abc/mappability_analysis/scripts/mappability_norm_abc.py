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

ref_file = '/projects/ps-renlab/nzemke/seurat/10x_multiome/mop_m1_integration/human/ATAC_bam/new_peaks/abc_score/neighborhoods_celltype_peaks/{}_neighborhoods/EnhancerList.txt'

bwavg = '/projects/ps-renlab2/earmand/conda_envs/bigwigtools/bin/bigWigAverageOverBed'
map_score = '../hg38/k100_map_score.bw'

# remove peaks below min map
min_map = .1 

for ct in cell_types:
    abc_ref = pd.read_csv(ref_file.format(ct), sep='\t')
    peak_bed = f'../mappability_intermediate_data/{ct}_peaks.bed'
    abc_ref[['chr', 'start', 'end', 'name']].to_csv(peak_bed,
                   header=None, index=None, sep='\t')
    
    map_quant_out = f'../mappability_intermediate_data/{ct}_mappability.txt'
    mapability_command = f'{bwavg} {map_score} {peak_bed} {map_quant_out}'
    os.system(mapability_command)
    
    map_quant = pd.read_csv(map_quant_out, sep='\t', header=None).set_index(0)
    abc_ref = abc_ref.set_index('name')
    abc_ref = abc_ref.join(map_quant[4].rename('mappability'))
    
    # threshold on mapability
    
    abc_ref = abc_ref.loc[abc_ref.mappability > .1]  
    
    abc_ref['norm_counts'] = abc_ref[f'ATAC.{ct}_merge_human_ATAC.bam.readCount']/abc_ref['mappability']
    
    abc_ref['norm_cpm'] = (abc_ref['norm_counts']*1e6)/abc_ref['norm_counts'].sum()

    abc_ref['activity_base_old'] = abc_ref['activity_base']
    abc_ref['activity_base'] = abc_ref['norm_cpm']
    
    abc_ref.reset_index().to_csv(f'../outs/mappability_norm_for_abc/{ct}_EnancerList.txt', sep='\t')