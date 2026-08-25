#!/bin/bash

# Request m nodes using n cores per node for n MPI tasks per node.

#SBATCH --job-name=igzo_sp
#SBATCH --nodes=32
#SBATCH --tasks-per-node=16
#SBATCH --cpus-per-task=8
#SBATCH --time=00:20:00

# Replace [budget code] below with your project code (e.g. t01)
#SBATCH --account=e05-bulk-shl
#SBATCH --partition=standard
#SBATCH --qos=short

# Setup the batch environment

module load cp2k/cp2k-2025.2

export OMP_NUM_THREADS=8
export OMP_PLACES=cores

# Ensure the cpus-per-task option is propagated to srun commands
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

srun --hint=nomultithread --distribution=block:block cp2k.psmp -i igzo_ordered_003_sp.inp >> igzo_ordered_003_sp.out