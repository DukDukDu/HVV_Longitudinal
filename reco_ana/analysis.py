import ROOT as R
from util import truth_filter_4tau2b_lepDecay_v2
from array import array
import anaconfig
import sampleconfig

class analysis(object):
  
    def __init__(self, ch, sampleID, nevent, basic_weight, outfnm ):
        self.chain = ch
        self.reader= R.ExRootTreeReader( self.chain )
        #     self.nevt = self.reader.GetEntries()
        self.procid = sampleID
        self.procnm = sampleconfig.id2proc_dict[sampleID]
        self.nevt = nevent
        self.weight = basic_weight

        # outputfile
        self.outfile = R.TFile(outfnm,'RECREATE')
        self.outtree = 0
        self.outlf = dict()

        # connters
        self.count_rawnb = 0 # int count raw number of events after truth filter if any

        # cutflow histogram
        self.cutflow_hist = R.TH1F('cutflow','Cutflow',50,0,50)
        self.cutflow_assigned = 0

    def fill_cut(self, cutnm):
        _ibin = self.cutflow_hist.GetXaxis().FindBin(cutnm)
        if _ibin == -1:
            self.cutflow_assigned += 1
            self.cutflow_hist.GetXaxis().SetBinLabel(self.cutflow_assigned, cutnm)
            self.cutflow_hist.SetBinContent( self.cutflow_assigned, 1 )
        else:
            self.cutflow_hist.SetBinContent( _ibin, self.cutflow_hist.GetBinContent(_ibin) + 1 )
        
    def mknewlf(self, varnm, vartype):
        # mknewlf("new_v", "F")
        # types: i, I, F
        # TODO add support for more types!!!
        if vartype == 'F':
            self.outlf[varnm] = array( 'f', [0] )
        elif vartype == 'I':
            self.outlf[varnm] = array( 'i', [0] )

        self.outtree.Branch(varnm, self.outlf[varnm], varnm+'/'+vartype)

    def fill_dummy(self):
        # fill dummy numbers to all declared leaevs
        for _lnm in self.outlf.keys():
            self.outlf[_lnm][0] = -999
        
    def begin(self):
        # branches
        self.br_electron = self.reader.UseBranch("Electron")
        self.br_muon = self.reader.UseBranch("Muon")
        self.br_jet = self.reader.UseBranch("Jet")
        self.br_genparticles = self.reader.UseBranch("Particle")
        self.br_missingET = self.reader.UseBranch("MissingET")
        self.br_event = self.reader.UseBranch("Event")
        # self.br_fatjet = self.reader.UseBranch("FatJet")

        # define outtree structure
        # 
        # NOTE: copying the old tree currently does not work
        # possible reasons: the copied leaves are not loaded as TreeReader do not load all br to accelerate
        # copy the whole input tree (TODO only copy some leaves not the whole)
        #self.chain.SetBranchStatus("*", 0) # de-activate all leaves of the input tree
        #self.chain.SetBranchStatus("Muon_size", 1) # active some leaves of the input tree
        #self.outtree = self.chain.CloneTree(0) # clone the structure
        #self.outtree.SetName('Events')
        #self.chain.SetBranchStatus("*", 1) # recover the whole input tree
        # 
        # Thus, create new tree atm
        self.outtree = R.TTree('Events','Events')

        # add new leaves
        self.mknewlf( 'weight', 'F' )
        self.mknewlf( 'dsid', 'I' )

        # channel specifics go into derived classes

    def loop(self):
        # overload it in derived classes
        pass

    def end(self):
        print('Run over {} events after truth filter if any'.format(self.count_rawnb))
        print('Total nb of evt loops: {}'.format(self.nevt))

        # save trees histograms
        self.outfile.Write()
        
        pass

    def sort_pt(self, lt_v4idx):
        # lt_v4idx is [ (v4, idx), ... ]
        # v4 is the lorentzvector of the particle
        # idx is the index of the particle in the original array from the input
        lt_v4idx.sort(key=lambda pi:pi[0].Pt(), reverse=True)