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
        R.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
        R.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')
    except:
        pass

    # parse arguments
    parser = argparse.ArgumentParser(description='Run analysis')
    parser.add_argument('process_name', type=str, help='Name of the process')
    parser.add_argument('ifile_list', type=str, help='List of input files')
    parser.add_argument('ofile_name', type=str, help='Name of the output file')
    parser.add_argument('--condor', action='store_true', help='Run with condor')
    args = parser.parse_args()

    _process_name = args.process_name
    _ifile_list = [int(i) for i in args.ifile_list.split(',')]
    _ofile_name = args.ofile_name
    _condor = args.condor

    print(f'Parallel runs with condor: {_condor}')
    anaconfig.global_config.condor = _condor

    print(anaconfig.global_config)

    filelist, sampleID = sample.getfilelist(_process_name)
    chain, basic_weight, event_number = sample.getchain(_process_name, 'Delphes', filelist, _ifile_list)

    print(basic_weight)

    ana = None
    if 'gg2e2m' in _process_name:
        print('Analysis type: gg2e2m')
        ana = analysis_gg2e2m.analysis_gg2e2m(chain, sampleID, event_number, basic_weight, _ofile_name)
    elif 'gg4e' in _process_name:
        print('Analysis type: gg4e')
        ana = analysis_gg4e.analysis_gg4e(chain, sampleID, event_number, basic_weight, _ofile_name)
    elif 'gg4m' in _process_name:
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
