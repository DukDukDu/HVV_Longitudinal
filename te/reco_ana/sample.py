import ROOT as R
from sampleconfig import *
import anaconfig
import os

def getfilelist(samplenm):
    print(f'Processing on {samplenm} ...\n')
    print(f'Storing in {os.path.join(data_path, sample_dict[samplenm])} / \n')
    file_list = []
    _files = os.listdir(os.path.join(data_path, sample_dict[samplenm]))
    _files.sort()

    for _file in _files:
        file_list.append(os.path.join(data_path, sample_dict[samplenm], _file.strip()))

    sampleID = "{:03d}".format(int(sample_dict[samplenm].split('.')[1]))
    print(f'Sample Index(SampleID) = {sampleID} \n')
    return file_list, sampleID

def weightCalc(samplenm, nevents):
    print('Calculating basic weights...\n')

    kFactor = kFactor_dict[samplenm]
    xsec = xsec_dict[samplenm]
    ntot = ntotal_dict[samplenm]
    procEff = eff_dict[samplenm]

    lumi = Lumi
    processedEvents = nevents

    if anaconfig.global_config.condor:
        intWeight = (kFactor * xsec * lumi) / (ntot * procEff)
    else:
        intWeight = (kFactor * xsec * lumi) / (ntot * procEff)

    return intWeight

def getchain(samplenm, treenm, filelist, ifile_list):
    chain = R.TChain(treenm)

    if len(ifile_list) > len(filelist):
        print(f'ERROR: file indices are more than nb of files in {os.path.join(data_path, sample_dict[samplenm])}')
        exit(1)

    for _ifile in ifile_list:
        chain.AddFile(filelist[_ifile])
        print(f'Add to chain {treenm} the file {filelist[_ifile]} \n')

    nfile = chain.GetNtrees()
    nevents = chain.GetEntries()

    print(f'In total loaded in {nfile} root files')
    print(f'In total loaded in {nevents} events')

    basic_weight = weightCalc(samplenm, nevents)

    return chain, basic_weight, nevents
