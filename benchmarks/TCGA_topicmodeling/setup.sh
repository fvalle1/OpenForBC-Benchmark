#!/bin/bash 

currPath=$(dirname "$0")
## PYTHON MODULES INSTALLATION ##
python3 -m pip install -r $currPath/requirements.txt

if [ -e $currPath/breast_cancer.tar.gz ]
then
    gunzip $currPath/breast_cancer.tar.gz
    tar -xvf $currPath/breast_cancer.tar
fi