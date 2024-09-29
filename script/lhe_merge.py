#It can be used for common needs, just change some code by YOURSELF.
#sys.argv[1] tot or bkg or sig
#sys.argv[2] gg2e2m or gg4m or gg4e
#sys.argv[3] name of job folder
#sys.argv[4] No. of mc folder
#!!!!del or mg must be in the sys.argv!!!!

import sys
import os

if 'mg' in sys.argv :
    mypub="/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/mg5condor/gg4l_{0}/{1}/{2}".format(sys.argv[1], sys.argv[2], sys.argv[3]) #this path is in ihep cluster
    rootfile = "{0}/rootfile".format(mypub)
    os.system("rm -rf {0} ; mkdir -p {0}".format(rootfile))
    
    #create lhe file path list
    file_list = []
    for i in range(100):
        file_list.append("{0}/{1}_{2}-0000{3:02d}".format(mypub, sys.argv[2], sys.argv[1], i))
    
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
    
    print("MADGRAPH PATH: You have converted {0} files and then you will hadd them......................".format(j))
    
    os.system("hadd {0}/total.root {0}/*.root".format(rootfile)) #hadd them into total.root file

elif 'del' in sys.argv:
    mypub="/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/delpycondor/gg4l_{0}/{1}/{2}".format(sys.argv[1], sys.argv[2], sys.argv[3])
    sample="/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/delpycondor/sample/mc.{0}.{1}_{2}.showersimul".format(sys.argv[4], sys.argv[2], sys.argv[1])

    file_list = []
    for i in range(100):
        file_list.append("{0}/{1}_{2}-0000{3:02d}".format(mypub, sys.argv[2], sys.argv[1], i))

    j = 0
    for f in file_list:
        os.system("ls {0} > {0}/out.txt".format(f))
        with open("{0}/out.txt".format(f), "r") as content:
            for line in content:
                if '.root' in line:
                    os.system("cp {0}/showersimul.root {1}/showersimul{2}.root".format(f, sample, j))
                    j +=1

    print("DELPHES PATH: You have copy {0} root files and then you will merge them..........................".format(j))

    os.system("hadd {0}/total.root {0}/showersimul*.root".format(sample))
    os.system("rm -f {0}/shower*".format(sample))

else:
    print("!!!!del or mg must be in the sys.argv, PLEASE CHECK YOUR INPUT!!!!")
