jobstring = """#!/bin/bash
#PBS -q condo
#PBS -l nodes=1:ppn=4                                                                                                      
#PBS -l walltime=8:00:00  
#PBS -o /home/nzemke/renlab2/multiome/mop_m1_integration/human_atac/motif_epi_conservation/job_log_distal/{0}.out
#PBS -e /home/nzemke/renlab2/multiome/mop_m1_integration/human_atac/motif_epi_conservation/job_log_distal/{0}.er
#PBS -N {0}_motif_conservation                     
#PBS -m n

source activate /home/nzemke/conda_envs/meme

cd /home/nzemke/renlab2/multiome/mop_m1_integration/human_atac/motif_epi_conservation/


#fimo --o fimo_output/{0}_fimo motif_files/JASPAR2022_CORE_vertebrates_non-redundant_pfms_meme/{0} human_union_atac_peaks.fa

cut -f3 fimo_output/{0}_fimo/fimo.tsv | sed 1d | sed 's/:/-/g' | grep '^chr' | LC_ALL=C fgrep -Fw -f - atac_cons_div_idx_mammal_level0_pairwise_round_distal.tsv > motif_cons_index_distal/{0}.tsv

cut -f2-13 motif_cons_index_distal/{0}.tsv | \
awk -F'\t' '{{                                    
    for(i = 1; i <= NF; i++) {{
        if($i != "NA" && $i ~ /^-?[0-9.]+$/) {{
            sum[i] += $i;
            count[i]++;
        }}
    }}
}}
END {{
    for(j = 1; j <= NF; j++) {{
        if(count[j] > 0) {{
            printf("%f\t", sum[j] / count[j]);
        }} else {{
            printf("NA\t");
        }}
    }}
}}' | paste -d '\t' <(printf "%s\\n" {0}) - > mean_cons_index_distal/{0}.tsv 

"""

import os
import sys

tfs = os.listdir('/home/nzemke/renlab2/multiome/mop_m1_integration/human_atac/motif_epi_conservation/motif_files/JASPAR2022_CORE_vertebrates_non-redundant_pfms_meme/')

job_name = '/home/nzemke/renlab2/multiome/mop_m1_integration/human_atac/motif_epi_conservation/qsub_files_distal/{0}.cmd'


for tf in tfs:
    open(job_name.format(tf), 'w+').write(jobstring.format(tf))
    os.system('qsub ' + job_name.format(tf))
