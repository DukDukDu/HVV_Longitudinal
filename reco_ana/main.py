import os
import sys
import sample
import analysis_gg2e2m
import analysis_gg4e
import analysis_gg4m
import ROOT as R
import argparse
import anaconfig

def main():
    R.gSystem.Load("libDelphes")
    try:
        ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
        ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
    except:
        pass

    # parse arguments
    _process_name = sys.argv[1]
    _ifile_list = sys.argv[2].split(',')
    _ifile_list = [ int(i) for i in _ifile_list ]
    _ofile_name = sys.argv[3]
    _addtional_args = sys.argv[4:]

    _condor = ('--condor' in sys.argv)
    print('Parallel runs with condor: {}'.format(_condor))
    anaconfig.global_config.condor = _condor

    print(anaconfig.global_config)

    filelist,sampleID = sample.getfilelist(_process_name)
    chain, basic_weight, event_number = sample.getchain(_process_name, 'Delphes', filelist, _ifile_list)

    print(basic_weight)

    ana = None
    if 'gg2e2m' in sys.argv:
        print('Analysis type: gg2e2m')
        ana = analysis_gg2e2m.analysis_gg2e2m(chain, sampleID, event_number, basic_weight, _ofile_name)
    elif 'gg4e' in sys.argv:
        print('Analysis type: gg4e')
        ana = analysis_gg4e.analysis_gg4e(chain, sampleID, event_number, basic_weight, _ofile_name)
    elif 'gg4m' in sys.argv:
        print('Analysis type: gg4m')
        ana = analysis_gg4m.analysis_gg4m(chain, sampleID, event_number, basic_weight, _ofile_name)
    else:
        print('No analysis type is defined (examples: gg2e2m, gg4e or gg4m). EXIT!')
        exit(1)

    ana.begin()
    ana.loop()
    ana.end()

if __name__ == '__main__':
    main()