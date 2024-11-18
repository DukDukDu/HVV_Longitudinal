# NOTE: this is to get the ntot of all events for each process
# local runs are quick without truth filters
# VERY SLOW for processes that has truth filters
# for all samples without truth filter, i.e. non HHbbmm
# :: python get_sampleinfo.py
# for the ones with truth filter, i.e. HHbbmm
# :: python get_sampleinfo_ihepcondor.py

from sampleconfig import *
from sample import *
import ROOT as R
import sys

R.gSystem.Load("libDelphes")
try:
    ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
    ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
except:
    pass

_dict = {}
_Np = 0
_Nn = 0
_sum_w = 0

# only for HHbbmm signals with condor runs
whichprocess = None
if len(sys.argv) >= 1:
  whichprocess = sys.argv[1]

print('whichprocess',whichprocess)

for _proc in sample_dict.keys():

  # skip HHbbmm signals, use condor instead !!!
  #if '--condor' not in sys.argv:
    # local, skip HHbbmm
    #if 'HHbbmm' in _proc:
      #continue
  #else:
    # condor, only process HHbbmm
    #if 'HHbbmm' not in _proc:
      #continue
    # only process whichHbbmm
  if whichprocess != _proc:
    continue

  _filelist, _sampleid = getfilelist(_proc)

  _chain = R.TChain('Delphes')
  for _fname in _filelist:
    _chain.AddFile( _fname )

  # samples in general
  _nevt = _chain.GetEntries()
  print(_nevt)
  _dict[_proc] = _nevt

  ## only for bbmm samples which have 4b 4muu and bbmm events
  # the following overwrite the above _dict[]

  if "2e2m" in _proc:
    _rd = R.ExRootTreeReader(_chain)
    _br_event = _rd.UseBranch("Event")
    for i in range(0, _nevt):
      _rd.ReadEntry(i)
      if _br_event[0].Weight > 0 :
        _Np += 1
      if _br_event[0].Weight < 0 :
        _Nn += 1
      _sum_w += _br_event[0].Weight
    _dict[_proc] = _sum_w

print('Copy the following to ntotal_dict in samplelist.py')
for _proc, _nevt in _dict.items():
  print("    '{0}' : {1},".format(_proc, _nevt))
print("Np = {}".format(_Np))
print("Nn = {}".format(_Nn))
print("Np + Nn = {}".format(_Np+_Nn))
print("Np - Nn = {}".format(_Np-_Nn))
print("Sum of Gen Event Weight is {}".format(_sum_w))