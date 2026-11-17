#!/bin/bash
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=32
#SBATCH --gres=gpu:4  # For TensorFlow surrogate
#SBATCH --time=24:00:00

module load cuda/11.8 openmpi/4.1.5
mpirun -np 128 python3 sim/parallel_launcher.py
