import ROOT as R
from util import truth_filter_4e
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools

class analysis_gg4e(analysis):

    def __init__(self, ch, sampleID, nevent, basic_weight, outfnm):
        analysis.__init__(self, ch, sampleID, nevent, basic_weight, outfnm)
        self.MUON_MASS = 0.1056583745  # PDG 2016 MOHR
        self.ELE_MASS = 0.0005109989461 # PDG 2016 MOHR

    def begin(self):
        analysis.begin(self)
        #add new leaves for gg2e2m
        analysis.mknewlf(self, 'e0_pt', 'F')
        analysis.mknewlf(self, 'e0_eta', 'F')
        analysis.mknewlf(self, 'e0_phi', 'F')
        analysis.mknewlf(self, 'e0_e', 'F')
        analysis.mknewlf(self, 'e1_pt', 'F')
        analysis.mknewlf(self, 'e1_eta', 'F')
        analysis.mknewlf(self, 'e1_phi', 'F')
        analysis.mknewlf(self, 'e1_e', 'F')
        analysis.mknewlf(self, 'e2_pt', 'F')
        analysis.mknewlf(self, 'e2_eta', 'F')
        analysis.mknewlf(self, 'e2_phi', 'F')
        analysis.mknewlf(self, 'e2_e', 'F')
        analysis.mknewlf(self, 'e3_pt', 'F')
        analysis.mknewlf(self, 'e3_eta', 'F')
        analysis.mknewlf(self, 'e3_phi', 'F')
        analysis.mknewlf(self, 'e3_e', 'F')

        analysis.mknewlf(self, 'inv_mass', 'F')

    def get_echarge(self, idx):
        return self.br_electron.At(idx).Charge
    
    def loof(self):

        for i in range(0, self.nevt):
            self.reader.ReadEntry(i)
            analysis.fill_cut(self, 'No cut')

            analysis.fill_dummy(self)

            evt_weight = self.weight

            lt_electron_sel = []

            e0_v4 = None
            e1_v4 = None
            e2_v4 = None
            e3_v4 = None
            tot_v4 = None

            #truth filter for gg4e
            if 'gg4e' in self.procnm:
                if truth_filter_4e(self.br_genparticles):
                    pass
                else:
                    continue
            analysis.fill_cut(self, 'truth filter')

            self.count_rawnb +=1

            for _ie in range(0, self.br_electron.GetEntries()):
                _e = self.br_electron.At(_ie)
                if _e.PT > 7 and abs(_e.eta) < 2.5:
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_e.PT, _e.Eta, _e.Phi, self.ELE_MASS)
                    lt_electron_sel.append((_v, _ie))

            analysis.sort_pt(self, lt_electron_sel)

            if len(lt_electron_sel) == 4:
                e0_v4 = lt_electron_sel[0][0]
                e1_v4 = lt_electron_sel[1][0]
                e2_v4 = lt_electron_sel[2][0]
                e3_v4 = lt_electron_sel[3][0]

            
            else:
                continue

            analysis.fill_cut(self, '4 electrons')

            tot_v4 = e0_v4 + e1_v4 + e2_v4 + e3_v4

            self.outlf['e0_pt'][0] = e0_v4.Pt()
            self.outlf['e0_eta'][0] = e0_v4.Eta()
            self.outlf['e0_phi'][0] = e0_v4.Phi()
            self.outlf['e0_e'][0] = e0_v4.E()
            self.outlf['e1_pt'][0] = e1_v4.Pt()
            self.outlf['e1_eta'][0] = e1_v4.Eta()
            self.outlf['e1_phi'][0] = e1_v4.Phi()
            self.outlf['e1_e'][0] = e1_v4.E()
            self.outlf['e2_pt'][0] = e2_v4.Pt()
            self.outlf['e2_eta'][0] = e2_v4.Eta()
            self.outlf['e2_phi'][0] = e2_v4.Phi()
            self.outlf['e2_e'][0] = e2_v4.E()
            self.outlf['e3_pt'][0] = e3_v4.Pt()
            self.outlf['e3_eta'][0] = e3_v4.Eta()
            self.outlf['e3_phi'][0] = e3_v4.Phi()
            self.outlf['e3_e'][0] = e3_v4.E()

            self.outlf['inv_mass'][0] = tot_v4.M()

            genweight = self.br_event.At(0)
            self.outlf['weight'][0] = evt_weight * genweight.Weight
            self.outlf['dsid'][0] = int(self.procid)

            self.outtree.Fill()

    def end(self):
        analysis.end(self)