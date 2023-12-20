#!/bin/bash

# get this shell script path
SCRIPT_PATH=$(cd $(dirname $0); pwd)

# fetch this folder
cd $SCRIPT_PATH

if [ -f $SCRIPT_PATH"/dev.flag" ]; then
    echo "This is DEV environment"
else
    echo "Activate the venv"
    source .venv/bin/activate
fi

LOG_FILE_NAME=$(date +'%Y-%m-%d_%H%M')

python jobs_cli.py --job_name zh_stock_min_price_load_job
