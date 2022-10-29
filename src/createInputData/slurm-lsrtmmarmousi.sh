#!/bin/sh

#SBATCH --job-name=nn                          # Job name
#SBATCH --nodes=1                              # Run all processes on 2 nodes
#SBATCH --partition=gpulongb                   # Partition OGBON
#SBATCH --output=out_%j.log                    # Standard output and error log
#SBATCH --ntasks-per-node=1                    # 1 job per node
#SBATCH --account=cenpes-lde                   # Account of the group

source "/opt/share/anaconda3/2022.05/etc/profile.d/conda.sh"
conda activate judi

srun julia --project=. lsrtm-marmousi.jl
