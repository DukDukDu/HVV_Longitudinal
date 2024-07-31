#!/bin/bash

jobdir=$1
procnm=$2
filelst=$3
anatype=$4
rootdir=$5

pwd
who
date
echo

cd ~/
pwd
#source ~/.bashrc
echo

cd $jobdir
pwd
ls
#source ${rootdir}/setup.sh
echo $PATH
echo $HOSTNAME
echo

echo 'check env via python'
python -c 'import os; print("HOSTNAME", os.getenv("HOSTNAME")); print(sorted(os.environ.keys()))'
echo

echo 'start the run'
echo "python $rootdir/main.py $procnm $filelst reco.root $anatype --condor"
python $rootdir/main.py $procnm $filelst reco.root $anatype --condor > output.log

echo 'end of the run'
echo

date
echo