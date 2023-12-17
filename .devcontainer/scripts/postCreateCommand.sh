#!/bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install vim -y

cd /workspaces/quant_yy
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
