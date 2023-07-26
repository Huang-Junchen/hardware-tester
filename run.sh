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
## Copyright (c) $(date +%Y) Neogenint Intelligent Co., Ltd.  ##
################################################################
"


ENV_NAME=venv
PYTHON_HOME=$ENV_NAME/bin/python


# Create python env
if [ -d "$ENV_NAME" ]; then
    echo "[INFO] Virtual environment already exists. Skipping creation step."
else
    echo "[INFO] Creating virtual environment..."
    python -m venv $ENV_NAME
fi

#source $ENV_NAME/bin/activate

echo "[INFO] Installing dependencies..."
sudo apt install -y lm-sensors
$PYTHON_HOME -m pip install --upgrade pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
$PYTHON_HOME -m pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

# Run python script
$PYTHON_HOME main.py "$@"