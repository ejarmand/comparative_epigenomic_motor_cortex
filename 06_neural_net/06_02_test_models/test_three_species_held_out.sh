#!/bin/bash

dataset_list=( 
    "human_all_mod"
    # "macaque_mcg_atac"
    # "marmoset_mcg_atac"
    # "mouse_all_mod"    
)

model_list=(
    "marmoset_macaque_mouse"
    # "human_marmoset_mouse_9"
    # "human_macaque_mouse_9_11"
    # "human_macaque_marmoset"
)

if $1; then
    GPU_USE=$1
    else
    GPU_USE=1
fi

N=31
numbers=$(seq -s, 0 $N)

for ((idx=0; idx<1; idx++)); do 
    model="${model_list[$idx]}"
    data="${dataset_list[$idx]}"
    species=( $(echo $model | cut -d "_" -f1,2,3 --output-delimiter=" ") ) 
    model_params="../models/json/three_species_multiomic_params.json"
    dataset="../datasets/${data}"
    
    echo "running"
#     model_out="../models/${model}/model0_best.h5"
#     test_out="../testing/loop_test/${model}_model_${species[0]}_head_${data}_predict/"

#     log="../logs/loop_logs/${model}_model_${species[0]}_head_${data}_test.log"

#     mkdir -p $test_out
#     test_str="CUDA_VISIBLE_DEVICES=${GPU_USE} python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save &> ${log}"
    
#     echo $test_str
#     eval $test_str
# # next species
#     model_out="../models/${model}/model1_best.h5"
#     test_out="../testing/loop_test/${model}_model_${species[1]}_head_${data}_predict/"

#     log="../logs/loop_logs${model}_model_${species[1]}_head_${data}_test.log"

#     mkdir -p $test_out
#     test_str="CUDA_VISIBLE_DEVICES=${GPU_USE} python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save &> ${log}"
    
#     echo $test_str
#     eval $test_str

# next species
    model_out="../models/${model}/model2_best.h5"
    test_out="../testing/loop_test/${model}_model_${species[2]}_head_${data2}_predict/"

    log="../logs/loop_logs${model}_model_${species[2]}_head_${data2}_test.log"

    mkdir -p $test_out
    test_str="CUDA_VISIBLE_DEVICES=${GPU_USE} python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save &> ${log}"
    
    echo $test_str
    eval $test_str        
done
