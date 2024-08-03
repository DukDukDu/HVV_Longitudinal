import ROOT as R
from util import truth_filter_4m
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools

class analysis_gg4m(analysis):

    def __init__(self, ch, sampleID, nevent, basic_weight, outfnm):
        analysis.__init__(self, ch, sampleID, nevent, basic_weight, outfnm)
        self.MUON_MASS = 0.1056583745  # PDG 2016 MOHR
        self.ELE_MASS = 0.0005109989461 # PDG 2016 MOHR

    def begin(self):
        analysis.begin(self)
        #add new leaves for gg2e2m
        analysis.mknewlf(self, 'mu0_pt', 'F')
        analysis.mknewlf(self, 'mu0_eta', 'F')
        analysis.mknewlf(self, 'mu0_phi', 'F')
        analysis.mknewlf(self, 'mu0_e', 'F')
        analysis.mknewlf(self, 'mu1_pt', 'F')
        analysis.mknewlf(self, 'mu1_eta', 'F')
        analysis.mknewlf(self, 'mu1_phi', 'F')
        analysis.mknewlf(self, 'mu1_e', 'F')
        analysis.mknewlf(self, 'mu2_pt', 'F')
        analysis.mknewlf(self, 'mu2_eta', 'F')
        analysis.mknewlf(self, 'mu2_phi', 'F')
        analysis.mknewlf(self, 'mu2_e', 'F')
        analysis.mknewlf(self, 'mu3_pt', 'F')
        analysis.mknewlf(self, 'mu3_eta', 'F')
        analysis.mknewlf(self, 'mu3_phi', 'F')
        analysis.mknewlf(self, 'mu3_e', 'F')

        analysis.mknewlf(self, 'inv_mass', 'F')

    def get_muoncharge(self, idx):
        return self.br_muon.At(idx).Charge

    def loof(self):

        for i in range(0, self.nevt):
            self.reader.ReadEntry(i)
            analysis.fill_cut(self, 'No cut')

            analysis.fill_dummy(self)

            evt_weight = self.weight

            lt_muon_sel = []

            mu0_v4 = None
            mu1_v4 = None
            mu2_v4 = None
            mu3_v4 = None
            tot_v4 = None

            if 'gg4m' in self.procnm:
                if truth_filter_4m(self.br_genparticles):
                    pass
                else:
                    continue

            analysis.fill_cut(self, 'truth filter')

            self.count_rawnb +=1

            for _imu in range(0, self.br_muon.GetEntries()):
                _mu = self.br_muon.At(_imu)
                if _mu.PT > 5 and abs(_mu.Eta) < 2.4:
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_mu.PT, _mu.Eta, _mu.Phi, self.MUON_MASS)
                    lt_muon_sel.append((_v, _imu))

            analysis.sort_pt(self, lt_muon_sel)

            if len(lt_muon_sel) == 4:
                mu0_v4 = lt_muon_sel[0][0]
                mu1_v4 = lt_muon_sel[1][0]
                mu2_v4 = lt_muon_sel[2][0]
                mu3_v4 = lt_muon_sel[3][0]

            else:
                continue

            analysis.fill_cut(self, '4 muons')

            tot_v4 = mu0_v4 + mu1_v4 + mu2_v4 + mu3_v4

            self.outlf['mu0_pt'][0] = mu0_v4.Pt()
            self.outlf['mu0_eta'][0] = mu0_v4.Eta()
            self.outlf['mu0_phi'][0] = mu0_v4.Phi()
            self.outlf['mu0_e'][0] = mu0_v4.E()
            self.outlf['mu1_pt'][0] = mu1_v4.Pt()
            self.outlf['mu1_eta'][0] = mu1_v4.Eta()
            self.outlf['mu1_phi'][0] = mu1_v4.Phi()
            self.outlf['mu1_e'][0] = mu1_v4.E()
            self.outlf['mu2_pt'][0] = mu2_v4.Pt()
            self.outlf['mu2_eta'][0] = mu2_v4.Eta()
            self.outlf['mu2_phi'][0] = mu2_v4.Phi()
            self.outlf['mu2_e'][0] = mu2_v4.E()
            self.outlf['mu3_pt'][0] = mu3_v4.Pt()
            self.outlf['mu3_eta'][0] = mu3_v4.Eta()
            self.outlf['mu3_phi'][0] = mu3_v4.Phi()
            self.outlf['mu3_e'][0] = mu3_v4.E()

            self.outlf['inv_mass'][0] = tot_v4.M()

            genweight = self.br_event.At(0)
            self.outlf['weight'][0] = evt_weight * genweight.Weight
            self.outlf['dsid'][0] = int(self.procid)

            self.outtree.Fill()

    def end(self):
        analysis.end(self)