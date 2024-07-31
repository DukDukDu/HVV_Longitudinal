import sys
import os
import re


def extract_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    patterns = {
        'original cross-section': r'# original cross-section:\s*([\d\.\-e]+)',
    }
    
    extracted_values = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            extracted_values[key] = float(match.group(1))
    
    return extracted_values

mypub="/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/mg5condor/gg4l_{0}/{1}/{2}".format(sys.argv[1], sys.argv[2], sys.argv[3]) #this path is in ihep cluster

file_list = []
for i in range(100):
    file_list.append("{0}/0000{1:02d}-run.out".format(mypub, i))

total = 0
j = 0

for f in file_list:
    numbers = extract_numbers_from_file("{0}".format(f))
    
    #j = j+1
    total = total + sum(numbers.values())

    if sum(numbers.values()) != 0:
        j = j+1

ave_xs = total/j
print("average xs is {0}, and total file is {1}".format(ave_xs, j))




