#!/bin/bash

dataset_list=( 
    "human_all_mod"
    "macaque_mcg_atac"
    "marmoset_mcg_atac"
     "mouse_all_mod"
)

specie_list=(
"human"
"macaque"
"marmoset"
"mouse"
)

N=31

if $1; then
    GPU_USE=$1
    else
    GPU_USE=2
fi

numbers=$(seq -s, 0 $N)

for ((i=0; i<4; i++)); do
# for data2 in "${dataset_list[@]}"; do
    data2="${dataset_list[i]}"
        # echo "running"
    model_params="../models/four_species_model_9_11/params.json"
    dataset="../datasets/${data2}"
    log="../logs/four_species_2_modality_${data2}_test.log"


    model_out="../models/four_species_model_9_11/model${i}_best.h5"
    specie_head="${species[i]}"
    test_out="../testing/four_species_2_modality/${specie_head}_model_${data2}_predict/"
    
    mkdir -p $test_out
    test_str="CUDA_VISIBLE_DEVICES=2 python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save &> ${log}"
    echo $test_str
    eval $test_str

    test_out="../testing/four_species_2_modality/${specie_head}_model_${data2}_predict/train_outs"
    
    mkdir -p $test_out
    test_str="CUDA_VISIBLE_DEVICES=2 python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save --split=train &> ${log}"
    echo $test_str
    eval $test_str

       test_out="../testing/four_species_2_modality/${specie_head}_model_${data2}_predict/val_outs"
    
    mkdir -p $test_out
    test_str="CUDA_VISIBLE_DEVICES=2 python ../basenji/bin/basenji_test.py -o ${test_out} --rc ${model_params} ${model_out} ${dataset} --ai $numbers --bi $numbers --save --split=valid &> ${log}"
    echo $test_str
    eval $test_str
    
    done
done
