#!/bin/sh

#SBATCH --job-name=lsrtm-marm                          # Job name
#SBATCH --nodes=1                              # Run all processes on 2 nodes
#SBATCH --partition=cpulongb                   # Partition OGBON
#SBATCH --output=out_%j.log                    # Standard output and error log
#SBATCH --ntasks-per-node=1                    # 1 job per node
#SBATCH --account=cenpes-lde                   # Account of the group

source "/opt/share/anaconda3/2022.05/etc/profile.d/conda.sh"
conda activate judi
export DEVITO_LOGGING=DEBUG
export DEVITO_ARCH="gcc"
export DEVITO_LANGUAGE="openmp"
module load gcc/11.1.0


srun julia --project=. lsrtm-marmousi.jl
