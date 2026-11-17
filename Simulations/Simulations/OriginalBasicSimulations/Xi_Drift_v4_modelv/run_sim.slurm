#!/bin/bash
#SBATCH --job-name=sim
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=16
#SBATCH --time=02:00:00
#SBATCH --output=job.out

module load mpi
source ~/.venv/bin/activate

mpirun -np 32 python -m physics_simulation --config configs/default.yml
