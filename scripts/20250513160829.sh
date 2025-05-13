#!/bin/bash
#$ -cwd
#$ -N 
#$ -l gpu_h=1
#$ -l h_rt=24:00:00
#$ -V
. /etc/profile.d/modules.sh
source  ~/.bashrc
module load cuda/12.1 cudnn/9.0.0
conda activate env
cd /mnt/d/lee_personal_things/qscriptor

python example.py \
  --batch_size 4 \
  --num_epochs 150 \
  --data_path ./dpdd_datasets/dpdd_dataset \
  --arg1 arg1 \
  --arg2 arg2 \
  --arg3 arg3