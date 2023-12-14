#!/bin/bash

dataset_list=( 
	"marmoset_multiome"
    "mouse_multiome"
    "human_well_covered"
    "macaque_multiome"
)

N=16

numbers=$(seq -s, 0 $N)

if [ -z "$1" ]; then
    GPU_USE=$(echo $1);
    else
    GPU_USE=2;
fi

for data1 in "${dataset_list[@]}"; do
    for data2 in "${dataset_list[@]}"; do
        echo "running"
        model_out="../models/loop_models/${data1}_model/model_best.h5"
        test_out="../testing/loop_test/${data1}_model_${data2}_predict/"
        model_params="../models/json/loop_params/${data1}_model.json"
        dataset="../datasets/${data2}"
        # n_outs=$(wc -l ${dataset}/targets.txt | awk '{print $1}')
        # let "n_outs=n_outs-1"
        log="../logs/loop_logs/${data1}_${data2}_test.log"
    
        # assuming the JSON file already exists and you want to modify it
        # jq '.model.head.units = '"$n_outs" "../models/json/large_resblock.json" >  $model_params
        mkdir -p $test_out
        test_str="CUDA_VISIBLE_DEVICES=${GPU_USE} python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save --peak &> ${log}"
        echo $test_str
        eval $test_str
    done
done

# dataset_list=( 
# 	"marmoset_multiome"
#     "mouse_multiome"
#     "human_well_covered"
#     "macaque_multiome"
# )

# N=16

# numbers=$(seq -s, 0 $N)

# for data1 in "${dataset_list[@]}"; do
#     for data2 in "${dataset_list[@]}"; do
#         if [ "$data1" == "$data2" ] &&  [[ "$data1" == *"human"* ]] ; do
#             echo "running"
#             model_out="../models/loop_models/${data1}_model/model_best.h5"
#             test_out="../testing/loop_test/${data1}_model_${data2}_predict/train_out"
#             model_params="../models/json/loop_params/${data1}_model.json"
#             dataset="../datasets/${data2}"
#             # n_outs=$(wc -l ${dataset}/targets.txt | awk '{print $1}')
#             # let "n_outs=n_outs-1"
#             log="../logs/loop_logs/${data1}_${data2}_test.log"
        
#             # assuming the JSON file already exists and you want to modify it
#             # jq '.model.head.units = '"$n_outs" "../models/json/large_resblock.json" >  $model_params
#             mkdir -p $test_out
#             test_str="CUDA_VISIBLE_DEVICES=${GPU_USE} python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save --split train &> ${log}"
#             echo $test_str
#             eval $test_str
#         fi
#     done
# done

# dataset_list=( 
# 	"marmoset_multiome"
#     "mouse_multiome"
#     "human_well_covered"
#     "macaque_multiome"
# )

# N=16

# numbers=$(seq -s, 0 $N)

# for data1 in "${dataset_list[@]}"; do
#     for data2 in "${dataset_list[@]}"; do
#         if [ "$data1" == "$data2" ] &&  [[ "$data1" == *"human"* ]] ; do
#             echo "running"
#             model_out="../models/loop_models/${data1}_model/model_best.h5"
#             test_out="../testing/loop_test/${data1}_model_${data2}_predict/valid_out"
#             model_params="../models/json/loop_params/${data1}_model.json"
#             dataset="../datasets/${data2}"
#             # n_outs=$(wc -l ${dataset}/targets.txt | awk '{print $1}')
#             # let "n_outs=n_outs-1"
#             log="../logs/loop_logs/${data1}_${data2}_test.log"
        
#             # assuming the JSON file already exists and you want to modify it
#             # jq '.model.head.units = '"$n_outs" "../models/json/large_resblock.json" >  $model_params
#             mkdir -p $test_out
#             test_str="CUDA_VISIBLE_DEVICES=${GPU_USE} python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save --split valid &> ${log}"
#             echo $test_str
#             eval $test_str
#         fi
#     done
# done