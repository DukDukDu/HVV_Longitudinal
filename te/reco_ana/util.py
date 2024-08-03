import os
import ROOT
import math
import importlib.util
import sys

def truth_filter_2e2m(genparticles):
    nbe = 0
    nbm = 0
    for particle in genparticles:
        if abs(particle.PID) == 11:
            nbe += 1
        if abs(particle.PID) == 13:
            nbm += 1
    
    if nbe >= 2 and nbm >= 2:
        return True
    return False

def truth_filter_zz_2e2m(genparticles):
    nbe = 0
    nbm = 0
    for particle in genparticles:
        if abs(particle.PID) == 11 and abs(genparticles[particle.M1].PID) == 23:
            nbe += 1
        if abs(particle.PID) == 13 and abs(genparticles[particle.M1].PID) == 23:
            nbm += 1

    if nbe == 2 and nbm == 2:
        return True
    return False

def truth_filter_4e(genparticles):
    nbe = 0
    for particle in genparticles:
        if abs(particle.PID) == 11:
            nbe += 1

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

# significance s/sqrt(b)
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
        # Taylor series expansion
        x = s / b
        y = (1 + x) * math.log(1 + x) - x
        if y < 0:
            y = (x**2) / 2 - (x**3) / 6 + (x**4) / 12 - (x**5) / 20 + (
                x**6) / 30 - (x**7) / 42
        return math.sqrt(2 * b * y)

# dynamic import
def dynamic_imp(name, class_name):
    try:
        spec = importlib.util.find_spec(name)
        if spec is None:
            print("Module not found: " + name)
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except ImportError as e:
        print(e)
        return None

