#!/usr/bin/env bash

rm pdf/$(ls pdf -t | head -n 1)

eval "$(conda shell.bash hook)"
conda activate $(basename $PWD)
./run.sh
git add .
git commit -m Update
git push
