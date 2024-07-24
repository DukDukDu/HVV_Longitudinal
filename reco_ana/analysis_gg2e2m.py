import ROOT as R
from util import truth_filter_2e2m
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools

class analysis_gg2e2m(analysis):

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

        analysis.mknewlf( self, 'mu0_pt', 'F' )
        analysis.mknewlf( self, 'mu0_eta', 'F' )
        analysis.mknewlf( self, 'mu0_phi', 'F' )
        analysis.mknewlf( self, 'mu0_e', 'F' )
        analysis.mknewlf( self, 'mu1_pt', 'F' )
        analysis.mknewlf( self, 'mu1_eta', 'F' )
        analysis.mknewlf( self, 'mu1_phi', 'F' )
        analysis.mknewlf( self, 'mu1_e', 'F' )

    def get_muoncharge(self, idx):
        return self.br_muon.At(idx).Charge

    def get_echarge(self, idx):
        return self.br_electron.At(idx).Charge

    def loop(self):

        for i in range(0, self.nevt):
            self.reader.ReadEntry(i)
            analysis.fill_cut(self, 'No cut')

            analysis.fill_dummy(self)

            evt_weight = self.weight

            lt_electron_sel = []
            lt_muon_sel = []

            e0_v4 = None
            e1_v4 = None
            mu0_v4 = None
            mu1_v4 = None
            
            #truth filter for gg2e2m
            if 'gg2e2m' in self.procnm:
                if truth_filter_2e2m(self.br_genparticles):
                    pass
                else:
                    continue
            analysis.fill_cut(self, 'truth filter')

            self.count_rawnb +=1

            for _ie in range(0, self.br_electron.GetEntries()):
                _e = self.br_electron.At(_ie)
                if _e.PT > 7 and abs(_e.eta) < 2.5:
                    _v = R.TLorentzVector()
                    -v.SetPtEtaPhiM(_e.PT, _e.Eta, _e.Phi, self.ELE_MASS)
                    lt_electron_sel.append((_v, _ie))

            analysis.sort_pt(self, lt_electron_sel)

            for _imu in range(0, self.br_muon.GetEntries()):
                _mu = self.br_muon.At(_imu)
                if _mu.PT > 5 and abs(_mu.Eta) < 2.4:
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_mu.PT, _mu.Eta, _mu.Phi, self.MUON_MASS)
                    lt_muon_sel.append((_v, _imu))

            analysis.sort_pt(self, lt_muon_sel)

            if len(lt_electron_sel) == 2:
                if self.get_echarge(lt_electron_sel[0][1])*self.get_echarge(lt_electron_sel[1][1]) < 0:
                    e0_v4 = lt_electron_sel[0][0]
                    e1_v4 = lt_electron_sel[1][0]

                else:
                    continue
            
            else:
                continue

            analysis.fill_cut(self, '2 oppo sign electron')

            if len(lt_muon_sel) == 2:
                if self.get_mucharge(lt_muon_sel[0][1])*self.get_mucharge(lt_muon_sel[1][1]) < 0:
                    mu0_v4 = lt_muon_sel[0][0]
                    mu1_v4 = lt_muon_sel[1][0]
                else:
                    continue

            else:
                continue

            analysis.fill_cut(self, '2 oppo sign muon')

            self.outlf['e0_pt'][0] = e0_v4.Pt()
            self.outlf['e0_eta'][0] = e0_v4.Eta()
            self.outlf['e0_phi'][0] = e0_v4.Phi()
            self.outlf['e0_e'][0] = e0_v4.E()
            self.outlf['e1_pt'][0] = e1_v4.Pt()
            self.outlf['e1_eta'][0] = e1_v4.Eta()
            self.outlf['e1_phi'][0] = e1_v4.Phi()
            self.outlf['e1_e'][0] = e1_v4.E()

            self.outlf['mu0_pt'][0] = mu0_v4.Pt()
            self.outlf['mu0_eta'][0] = mu0_v4.Eta()
            self.outlf['mu0_phi'][0] = mu0_v4.Phi()
            self.outlf['mu0_e'][0] = mu0_v4.E()
            self.outlf['mu1_pt'][0] = mu1_v4.Pt()
            self.outlf['mu1_eta'][0] = mu1_v4.Eta()
            self.outlf['mu1_phi'][0] = mu1_v4.Phi()
            self.outlf['mu1_e'][0] = mu1_v4.E()

            genweight = self.br_event.At(0)
            self.outlf['weight'][0] = evt_weight * genweight.Weight
            self.outlf['dsid'][0] = int(self.procid)

            self.outtree.Fill()

    def end(self):
        analysis.end(self)