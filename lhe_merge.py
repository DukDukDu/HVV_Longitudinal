#To run this script you need python env and you should give two input virables.
#The first is tot/bkg/sig or other strings you define, and the second is gg2e2m/gg4m/gg4e or other strings you define.
#It can be used for common needs, just change some code by YOURSELF.

import sys
import os

mypub="/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/mg5condor/gg4l_{0}/{1}/jobs".format(sys.argv[1], sys.argv[2]) #this path is in ihep cluster
rootfile = "{0}/rootfile".format(mypub)
os.system("rm -rf {0} ; mkdir -p {0}".format(rootfile))

#create lhe file path list
file_list = []
for i in range(100):
    file_list.append("{0}/gg2e2m_tot-0000{1:02d}".format(mypub, i))

#ls the dir to out.txt and read out.txt to examine if the lhe file exists
j=0
for f in file_list:
    os.system("ls {0} > {0}/out.txt".format(f))
    with open("{0}/out.txt".format(f), "r") as content:
        for line in content:
            if '.lhe' in line:
                os.system("/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/mg5condor/ExRootAnalysis/ExRootLHEFConverter \
                {0}/cmsgrid_final.lhe {1}/cmsfinal{2:02d}.root".format(f, rootfile, j)) #convert lhe files into root files
                j = j+1

print("You have converted {0} files and then you will hadd them......................".format(j+1))

os.system("hadd {0}/total.root {0}/*.root".format(rootfile)) #hadd them into total.root file
