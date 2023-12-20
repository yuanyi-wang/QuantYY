#!/bin/bash

# get this shell script path
PROJECT_ROOT=$(cd $(dirname $0); pwd)

# fetch this folder
cd $PROJECT_ROOT

if [ -f $PROJECT_ROOT"/dev.flag" ]; then
    echo "This is DEV environment"
else
    echo "Activate the venv"
    source .venv/bin/activate
fi

python all_tests.py