import sys
import os

mypub="/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/mg5condor/gg4l_{0}/{1}/{2}".format(sys.argv[1], sys.argv[2], sys.argv[3]) #this path is in ihep cluster

file_list = []
for i in range(100):
    file_list.append("{0}/{1}_{2}-0000{3:02d}".format(mypub, sys.argv[2], sys.argv[1], i))

for f in file_list:
    sub_files = os.listdir(f)
    #print(sub_files)
    for sub_file in sub_files:
        if sub_file == "cmsgrid_final.lhe":
            continue
        else:
            os.system("rm -rf {0}/{1}".format(f, sub_file))
