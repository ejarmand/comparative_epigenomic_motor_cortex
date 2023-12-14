#!/bin/bash

data_list0=(  
	# "marmoset_multiome"
 #    "mouse_multiome"
 #    "human_well_covered"
    # "macaque_multiome"
)

data_list1=(  
    # "human_mcg"
    # "marmoset_mcg"
    # "mouse_mcg"
    # "macaque_mcg"
    "macaque_multiome"
    
)

data_list2=(  
    # "human_all_mod"
    # "mouse_all_mod"
    # "marmoset_mcg_atac"
    # "macaque_mcg_atac"
)

for data1 in "${data_list1[@]}"; do
    echo $data1
    
    for data2 in "${data_list1[@]}"; do
        specie=$(echo $data2 | cut -d "_" -f1 --output-delimiter=" ") 
        pred_bedgraph="../testing/loop_test/${data1}_model_${data2}_predict/bedgraph/"
        peaks_in="../datasets/ref_data/peak_sets/union_${specie}_ATAC_peaks_SPM_${specie}_blacklist_filtered.bed"
        peaks_out="../testing/loop_test/${data1}_model_${data2}_predict/peak_outs/"
        
        eval_str="bash aggregate_peaks.sh ${pred_bedgraph} ${peaks_in} ${peaks_out}"
        echo $eval_str
        eval $eval_str
    done
done

# for data1 in "${data_list2[@]}"; do
#     for data2 in "${data_list2[@]}"; do
#         specie=$(echo $data2 | cut -d "_" -f1 --output-delimiter=" ") 
#         pred_bedgraph="../testing/loop_test/${data1}_model_${data2}_predict/bedgraph/"
#         peaks_in="../datasets/ref_data/peak_sets/union_${specie}_ATAC_peaks_SPM_${specie}_blacklist_filtered.bed"
#         peaks_out="../testing/loop_test/${data1}_model_${data2}_predict/peak_outs/"
        
#         eval_str="bash aggregate_peaks.sh ${pred_bedgraph} ${peaks_in} ${peaks_out}"
#         echo $eval_str
#         eval $eval_str
#     done
# done

# for data1 in "${data_list0[@]}"; do
#     for data2 in "${data_list0[@]}"; do
#         specie=$(echo $data2 | cut -d "_" -f1 --output-delimiter=" ") 
#         pred_bedgraph="../testing/loop_test/${data1}_model_${data2}_predict/bedgraph/"
#         peaks_in="../datasets/ref_data/peak_sets/union_${specie}_ATAC_peaks_SPM_${specie}_blacklist_filtered.bed"
#         peaks_out="../testing/loop_test/${data1}_model_${data2}_predict/peak_outs/"
        
#         eval_str="bash aggregate_peaks.sh ${pred_bedgraph} ${peaks_in} ${peaks_out}"
#         echo $eval_str
#         eval $eval_str
#     done
# done



