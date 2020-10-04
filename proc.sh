#!/usr/bin/env bash

eval "$(conda shell.bash hook)"
conda activate $(basename $PWD)
./run.sh
git add .
git commit -m Update
git push
