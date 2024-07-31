import os
import ROOT
import math
import imp
import sys

def truth_filter_2e2m(genparticles):
    nbe = 0
    nbm = 0
    lis = []
    for particle in genparticles:

        lis.append(particle.PID)
        if abs(particle.PID) == 11:
            nbe +=1
        if abs(particle.PID) == 13:
            nbm +=1
        
    #print('000000000000000000000000000000000')
    #print("{0}, {1}".format(nbe, nbm))
    if nbe >= 2 and nbm >= 2 :
        return True
    return False

def truth_filter_zz_2e2m(genparticles):
    nbe = 0
    nbm = 0
    for particle in genparticles:
        if abs(particle.PID) == 11 and abs(genparticles[particle.M1].PID) == 23:
            nbe += 1

        if abs(particle.PID) == 11 and abs(genparticles[particle.M1].PID) == 23:
            nbm += 1

    if nbe == 2 and nbm == 2:
        return True
    return False

def truth_filter_4e(genparticles):
    nbe = 0
    for particle in genparticles:
        if abs(particle.PID) == 11:
            nbe +=1

    if nbe >= 4:
        return True
    return False

def truth_filter_4m(genparticles):
    nbm = 0
    for particle in genparticles:
        if abs(particle.PID) == 13:
            nbm += 1
    
    if nbm >= 4:
        return True
    return False


# significane s/sqrt(b)
def sig_sob(s, b):
    if b <= 0:
        return 0
    else:
        return s / math.sqrt(b)


# significance new sob
def newsig_sob(s, b):
    if b == 0:
        return 0
    else:
        # Tylor series expansion
        x = s / b
        y = (1 + x) * math.log(1 + x) - x
        if y < 0:
            y = (x**2) / 2 - (x**3) / 6 + (x**4) / 12 - (x**5) / 20 + (
                x**6) / 30 - (x**7) / 42
        return math.sqrt(2 * b * y)

# dynamic import
def dynamic_imp(name, class_name):

    # find_module() method is used
    # to find the module and return
    # its description and path
    try:
        fp, path, desc = imp.find_module(name)
    except ImportError:
        print("module not found: " + name)

    # load_modules loads the module
    # dynamically and takes the filepath
    # module and description as parameter
    try:
        example_package = imp.load_module(name, fp, path, desc)
    except Exception as e:
        print(e)

    #try:
    #    myclass = imp.load_module("% s.% s" % (name,class_name), fp, path, desc)
    #except Exception as e:
    #    print(e)

    return example_package  #, myclass
