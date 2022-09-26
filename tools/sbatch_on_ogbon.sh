#!/usr/bin/env nix-shell
#!nix-shell -i sh -p rsync git

TOPLEVEL=$(git rev-parse --show-toplevel)
FOLDER=${TOPLEVEL##*/}

rsync --progress --delete -r --exclude .julia "$TOPLEVEL" ogbon:~/

ssh ogbon "cd ~/$FOLDER; sbatch slurm.sh"
