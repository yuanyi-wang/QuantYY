#!/bin/bash

sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
sudo cp apt-sources.list /etc/apt/sources.list

cp -r .devcontainer/home/.pip ~