#!/bin/bash

# get this shell script path
SCRIPT_PATH=$(cd $(dirname $0); pwd)

# fetch this folder
cd $SCRIPT_PATH

source .venv/bin/activate

python src/2mins_data_analysis.py
