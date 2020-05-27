#!/usr/bin/env bash

python download.py
python analyze.py
jupyter nbconvert --to notebook --inplace --execute visualize.ipynb