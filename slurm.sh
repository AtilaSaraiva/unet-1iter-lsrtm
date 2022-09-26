#!/bin/sh

#SBATCH --job-name=nn                          # Job name
#SBATCH --nodes=1                              # Run all processes on 2 nodes
#SBATCH --partition=gpulongb                   # Partition OGBON
#SBATCH --output=out_%j.log                    # Standard output and error log
#SBATCH --ntasks-per-node=1                    # 1 job per node
#SBATCH --account=cenpes-lde                   # Account of the group

#NIXPKGS_ALLOW_UNFREE=1 nix-portable nix-shell --command "cd src && make"
#NIXPKGS_ALLOW_UNFREE=1 nix-portable nix-shell --command "cd src/createInputData && julia --project=. createInputData.jl"
NIXPKGS_ALLOW_UNFREE=1 nix-portable nix-shell --command "cd src && python space_domain_train.py"
