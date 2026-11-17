#!/bin/bash
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --time=24:00:00

module load cuda/12.2 openmpi/4.1.5
mpirun -n 128 \
    python3 sim/parallel_launcher.py \
    --surrogate-model models/surrogate_xi.keras
