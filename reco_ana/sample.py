import ROOT as R
from sampleconfig import *
import anaconfig
import os

def getfilelist(samplenm):
    
    print('Processing on '+samplenm+' ...\n')
    print('Storing in '+data_path+sample_dict[samplenm] + '/ \n')
    file_list = []
    _files = os.listdir(os.path.join(data_path,sample_dict[samplenm]))
    _files.sort()
    
    for _file in _files:
        file_list.append(os.path.join(data_path , sample_dict[samplenm] , _file.strip()))
    #end
    
    sampleID = "%03d" % int(sample_dict[samplenm].split('.', -1)[1])
    print('Sample Index(SampleID) = ' + str(sampleID) + ' \n')
    return file_list, sampleID
#END

def weightCalc(samplenm, nevents):
    print('Calculating basic weights...\n')
    
    kFactor = kFactor_dict[samplenm]
    xsec    = xsec_dict[samplenm]
    ntot    = ntotal_dict[samplenm]
    procEff         = eff_dict[samplenm]

    lumi    = Lumi
    
    processedEvents = nevents
    
    # with condor parallel runs, divide by total events of all samples
    if anaconfig.global_config.condor:
      intWeight = (kFactor*xsec*lumi)/(ntot*procEff)
    # with local single runs, divide by nb of events loaded to this run
    else:
      #intWeight = (kFactor*xsec*Br*lumi)/(processedEvents*procEff)
      intWeight = (kFactor*xsec*lumi)/(ntot*procEff)
    
    return intWeight
#END

# tree name and a file that contains names of all input root files
def getchain( samplenm, treenm, filelist, ifile_list ):
    chain = R.TChain( treenm )

    if len(ifile_list) > len(filelist):
      print('ERROR: file indices are more than nb of files in {}'.format(data_path + sample_dict[samplenm]))
      exit(1)
    
    for _ifile in ifile_list:
        chain.AddFile( filelist[_ifile] )
        print('Add to chain {0} the file {1} \n'.format( treenm, filelist[_ifile] ))
    
    nfile = chain.GetNtrees()
    nevents = chain.GetEntries()

    print('In total loaded in {0} root files'.format(nfile) )
    print('In total loaded in {0} events'.format(nevents) )
    
    basic_weight = weightCalc(samplenm, nevents)
        
    return chain, basic_weight, nevents
#END