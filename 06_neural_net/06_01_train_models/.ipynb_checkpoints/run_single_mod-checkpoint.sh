#!/bin/bash

dataset_list=( 
            "marmoset_multiome"
            "mouse_multiome"
            "human_well_covered"
            "macaque_multiome"

            "mouse_all_mod"
            "human_all_mod"
            "marmoset_mcg_atac"
            "macaque_mcg_atac"
	)


for data in "${dataset_list[@]}"; do
    model_out="../models/loop_models/${data}_model"
    model_params="../models/json/loop_params/${data}_model.json"
    model_test="../testing/loop_tests/${data}_model"
    dataset="../datasets/${data}"
    n_outs=$(wc -l ${dataset}/targets.txt | awk '{print $1}')
    let "n_outs=n_outs-1"
    log="../logs/loop_logs/${data}_train.log"

    # assuming the JSON file already exists and you want to modify it
    jq '.model.head.units = '"$n_outs" "../models/json/large_resblock.json" >  $model_params

    train_str="CUDA_VISIBLE_DEVICES=0 /home/earmand/conda_envs/basenji_tf/bin/python /home/earmand/projects/basenji/basenji/bin/basenji_train.py -o ${model_out} ${model_params} ${dataset} &> ${log}"
    echo $train_str
    eval $train_str
done
