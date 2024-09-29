# HZZ Longitudinal
All of the files is written for HZZ Longitudinal analysis. And there are 9 processes i.e. gg->2e2m(sig, bkg, tot), 
gg->4e(sig, bkg, tot) and gg->4m(sig, bkg, tot).

# lhe level analysis
lhe level analysis codes are in the **lhe_ana** folder. *read_lhe_zz.h* is used to handle two on-shell z final state, 
while *read_lhe_4l.h* is used to handle 4 leptons final state. *draw.h* is used to draw some kinematic variables. You
can include these files in the *inter.c*. **./pic** is used to store some pictures.

# reco level analysis
reco level analysis codes are in the **reco_ana** and are written in Python. The details about the analysis code can be found 
in the readme of HH-ANA *https://github.com/xiaohu-cern/HH-Ana/tree/main*. But there are still some changes. My code has been modified
and can be run in python3 env. MELA(matrix element likelihood approach) analysis code is added in and you can find the tutorial MELA
code in **../MELA**. More details about MELA can be found in *https://spin.pha.jhu.edu/MELA/*. **./limit** is used to store the limit-calculating code. **./pic** is used to store some pictures. *Draw.c* is used to draw some kinematic variables from the reco level root files which are handled by analysis_xxxx.py already.

# script
Some scripts are put in the folder **script**. *cal_xs.py* is used to calculate average cross sections from the condor jobs' output files
in lhe level. *lhe_merge.py* is used to merge lhe files into root files in order for analysis and drawing kinematic variables in lhe level,
and merge root files after Pythia and Delphes into a bigger root files in order for reco level analysis. *folder_rm.py* is used to remove trash
files produced in condor jobs.

# MC
The *run_card.dat* used in genproduction can be found here. *setcut.f* is the source file of MadGraph, and we modified this file. If you want to use this 
file in your MadGraph, please copy them into correct folder before compile your MadGraph. *config_HVV_Longitudinal.cmnd* is the Pythia card and *delphes_card_CMS.tcl*
is the Delphes card for CMS.

# Final
You must run the code in the correct env. You'd better use conda to create your own virtual env.  
'''
conda config --set channel_priority strict
conda create -c conda-forge --name myroot root
conda activate myroot
'''  
And you also need Delphes built up in your env:
'''
wget http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.5.0.tar.gz
tar -zxf Delphes-3.5.0.tar.gz

cd Delphes-3.5.0
mkdir -p build
cd build

cmake -DCMAKE_INSTALL_PREFIX=/your/conda/env/path ..
make -j 4 install
'''  
And you also need MELA built up in your env. Below commands are run in the *JHUGenerator.v7.5.6/JHUGenMELA/* :
'''
./setup.sh
'''  
Then you follow the instructions printed on the screen, and you will build up MELA easily. And before you use MELA, you 
should add the env paths using command.