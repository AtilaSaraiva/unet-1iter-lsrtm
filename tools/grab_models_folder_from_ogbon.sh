#!/usr/bin/env nix-shell
#!nix-shell -i sh -p rsync git

TOPLEVEL=$(git rev-parse --show-toplevel)
FOLDER=${TOPLEVEL##*/}

rsync --progress --delete -r ogbon:~/$FOLDER/models $TOPLEVEL/
