#!/bin/bash
echo "
################################################################
## Script Description:                                        ##
## This script is for recording the GPU and CPU temperature   ##
## and utilization during burning testing.                    ##
##                                                            ##
## Author:              Jason Huang                           ##
## Last Modified:       July 25, 2023                         ##
##                                                            ##
## Copyright (c) $(date +%Y) Neogenint Intelligent Co., Ltd.         ##
################################################################
"


ENV_NAME=venv
PYTHON_HOME=$ENV_NAME/bin/python
GPU_BURN_FOLDER=gpu-burn


# Create python env
if [ -d "$ENV_NAME" ]; then
    echo -e "\033[92m[INFO] Virtual environment already exists. Skipping creation step.\033[0m"
else
    echo -e "\033[92m[INFO] Creating virtual environment...\033[0m"
    python -m venv $ENV_NAME
    echo -e "\033[92m[INFO] Installing dependencies...\033[0m"
    sudo apt install -y lm-sensors
    $PYTHON_HOME -m pip install --upgrade pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
    $PYTHON_HOME -m pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
fi

if [ -d "$GPU_BURN_FOLDER" ]; then
    echo -e "\033[92m[INFO] gpu-burn has already installed.\033[0m"
else
    echo -e "\033[92m[INFO] installing gpu-burn.\033[0m"
    git clone https://github.com/wilicc/gpu-burn.git
    cd gpu-burn
    make
    cd ..
fi


#source $ENV_NAME/bin/activate

# Run python script
$PYTHON_HOME gui.py "$@"