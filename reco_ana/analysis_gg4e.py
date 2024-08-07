import ROOT as R
from util import lep_pair
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools
import numpy as np
import Mela

class analysis_gg4e(analysis):
    mela = Mela.Mela(13, 125, Mela.VerbosityLevel.SILENT)

    def __init__(self, ch, sampleID, nevent, basic_weight, outfnm):
        analysis.__init__(self, ch, sampleID, nevent, basic_weight, outfnm)
        self.MUON_MASS = 0.1056583755  # PDG 2023 MOHR
        self.ELE_MASS = 0.00051099895000 # PDG 2023 MOHR
        self.Z_MASS = 91.1876

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
        analysis.mknewlf(self, 'ee1_inv_mass', 'F')
        analysis.mknewlf(self, 'ee2_inv_mass', 'F')
        analysis.mknewlf(self, 'ee1_pt', 'F')
        analysis.mknewlf(self, 'ee2_pt', 'F')
        analysis.mknewlf(self, 'delta_ee1_eta', 'F')
        analysis.mknewlf(self, 'delta_ee2_eta', 'F')
        analysis.mknewlf(self, 'delta_ee1_phi', 'F')
        analysis.mknewlf(self, 'delta_ee2_phi', 'F')

        analysis.mknewlf(self, 'probsig', 'F')
        analysis.mknewlf(self, 'probbkg', 'F')
        analysis.mknewlf(self, 'D_value', 'F')

    def get_echarge(self, idx):
        return self.br_electron.At(idx).Charge
    
    def loop(self):

        for i in range(0, self.nevt):
            self.reader.ReadEntry(i)
            analysis.fill_cut(self, 'No cut')

            analysis.fill_dummy(self)

            evt_weight = self.weight

            lt_electron_sel = []
            lt_z1 = []
            lt_z2 = []

            e0_v4 = None
            e1_v4 = None
            e2_v4 = None
            e3_v4 = None
            ee1_v4 = None
            ee2_v4 = None
            tot_v4 = None

            pdgid = []
            daughtersPt = []
            daughtersEta = []
            daughtersPhi = []
            daughtersMass = []

            mz11=0
            mz12=0
            mz21=0
            mz22=0
            mz31=0
            mz32=0

            self.count_rawnb +=1

            for _ie in range(0, self.br_electron.GetEntries()):
                _e = self.br_electron.At(_ie)
                if _e.PT > 7 and abs(_e.Eta) < 2.5:
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_e.PT, _e.Eta, _e.Phi, self.ELE_MASS)
                    lt_electron_sel.append((_v, _ie))
                    daughtersPt.append(_e.PT)
                    daughtersEta.append(_e.Eta)
                    daughtersPhi.append(_e.Phi)
                    daughtersMass.append(self.ELE_MASS)
                    if self.get_echarge(_ie) < 0:
                        pdgid.append(11)
                    else:
                        pdgid.append(-11)

            analysis.sort_pt(self, lt_electron_sel)

            if len(lt_electron_sel) == 4:
                e0_v4 = lt_electron_sel[0][0]
                e1_v4 = lt_electron_sel[1][0]
                e2_v4 = lt_electron_sel[2][0]
                e3_v4 = lt_electron_sel[3][0]

                if self.get_echarge(lt_electron_sel[0][1])*self.get_echarge(lt_electron_sel[1][1]) < 0:
                    mz11 = (e0_v4 + e1_v4).M()
                    mz12 = (e2_v4 + e3_v4).M()

                if self.get_echarge(lt_electron_sel[0][1])*self.get_echarge(lt_electron_sel[2][1]) < 0:
                    mz21 = (e0_v4 + e2_v4).M()
                    mz22 = (e1_v4 + e3_v4).M()

                if self.get_echarge(lt_electron_sel[0][1])*self.get_echarge(lt_electron_sel[3][1]) < 0:
                    mz31 = (e0_v4 + e3_v4).M()
                    mz32 = (e1_v4 + e2_v4).M()

                dl1 = np.sqrt((self.Z_MASS - mz11)**2 + (self.Z_MASS - mz12)**2)
                dl2 = np.sqrt((self.Z_MASS - mz21)**2 + (self.Z_MASS - mz22)**2)
                dl3 = np.sqrt((self.Z_MASS - mz31)**2 + (self.Z_MASS - mz32)**2)

                ee1_v4, ee2_v4, lt_z1, lt_z2 = lep_pair(dl1, dl2, dl3, e0_v4, e1_v4, e2_v4, e3_v4)

            else:
                continue

            analysis.fill_cut(self, '4 electrons')

            mothers = None
            associated = None
            daughters = Mela.SimpleParticleCollection_t(pdgid, daughtersPt, daughtersEta, daughtersPhi, daughtersMass, True)
            
            self.mela.setInputEvent(daughters, associated, mothers, True)
            self.mela.setProcess(Mela.Process.HSMHiggs, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            probsig = self.mela.computeP(False)

            self.mela.setProcess(Mela.Process.bkgZZ, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            probbkg = self.mela.computeP(False)

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
            self.outlf['ee1_inv_mass'][0] = ee1_v4.M()
            self.outlf['ee2_inv_mass'][0] = ee2_v4.M()
            self.outlf['ee1_pt'][0] = ee1_v4.Pt()
            self.outlf['ee2_pt'][0] = ee2_v4.Pt()
            self.outlf['delta_ee1_eta'][0] = abs(lt_z1[0][0].Eta()-lt_z1[1][0].Eta())
            self.outlf['delta_ee2_eta'][0] = abs(lt_z2[0][0].Eta()-lt_z2[1][0].Eta())
            self.outlf['delta_ee1_phi'][0] = abs(lt_z1[0][0].Phi()-lt_z1[1][0].Phi())
            self.outlf['delta_ee2_phi'][0] = abs(lt_z2[0][0].Phi()-lt_z2[1][0].Phi())

            self.outlf['probsig'][0] = probsig
            self.outlf['probbkg'][0] = probbkg
            self.outlf['D_value'][0] = probsig/(probbkg+probsig)

            genweight = self.br_event.At(0)
            self.outlf['weight'][0] = evt_weight * genweight.Weight
            self.outlf['dsid'][0] = int(self.procid)

            self.outtree.Fill()

    def end(self):
        analysis.end(self)
