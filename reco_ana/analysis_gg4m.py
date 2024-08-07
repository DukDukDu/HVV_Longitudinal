import ROOT as R
from util import lep_pair
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools
import Mela

class analysis_gg4m(analysis):
    mela = Mela.Mela(13, 125, Mela.VerbosityLevel.SILENT)

    def __init__(self, ch, sampleID, nevent, basic_weight, outfnm):
        super().__init__(ch, sampleID, nevent, basic_weight, outfnm)
        self.MUON_MASS = 0.1056583755  # PDG 2023 MOHR
        self.ELE_MASS = 0.00051099895000 # PDG 2023 MOHR
        self.Z_MASS = 91.1876

    def begin(self):
        super().begin()
        # add new leaves for gg2e2m
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
        
        analysis.mknewlf('inv_mass', 'F')
        analysis.mknewlf(self, 'inv_mass', 'F')
        analysis.mknewlf(self, 'mumu1_inv_mass', 'F')
        analysis.mknewlf(self, 'mumu2_inv_mass', 'F')
        analysis.mknewlf(self, 'mumu1_pt', 'F')
        analysis.mknewlf(self, 'mumu2_pt', 'F')
        analysis.mknewlf(self, 'delta_mumu1_eta', 'F')
        analysis.mknewlf(self, 'delta_mumu2_eta', 'F')
        analysis.mknewlf(self, 'delta_mumu1_phi', 'F')
        analysis.mknewlf(self, 'delta_mumu2_phi', 'F')

        analysis.mknewlf(self, 'prob', 'F')

    def get_muoncharge(self, idx):
        return self.br_muon.At(idx).Charge

    def loop(self):
        for i in range(self.nevt):
            self.reader.ReadEntry(i)
            self.fill_cut('No cut')

            self.fill_dummy()

            evt_weight = self.weight

            lt_muon_sel = []
            lt_z1 = []
            lt_z2 = []

            mu0_v4 = None
            mu1_v4 = None
            mu2_v4 = None
            mu3_v4 = None
            mumu1_v4 = None
            mumu2_v4 = None
            tot_v4 = None

            pdgid = []
            daughtersPt = []
            daughtersEta = []
            daughtersPhi = []
            daughtersMass = []

            mz11 =0 
            mz12 = 0
            mz21 = 0
            mz22 = 0
            mz31 = 0
            mz32 = 0

            self.count_rawnb += 1

            for _imu in range(self.br_muon.GetEntries()):
                _mu = self.br_muon.At(_imu)
                if _mu.PT > 5 and abs(_mu.Eta) < 2.4:
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_mu.PT, _mu.Eta, _mu.Phi, self.MUON_MASS)
                    lt_muon_sel.append((_v, _imu))
                    daughtersPt.append(_mu.PT)
                    daughtersEta.append(_mu.Eta)
                    daughtersPhi.append(_mu.Phi)
                    daughtersMass.append(self.MUON_MASS)
                    if self.get_muoncharge(_imu) < 0:
                        pdgid.append(13)
                    else:
                        pdgid.append(-13)

            self.sort_pt(lt_muon_sel)

            if len(lt_muon_sel) == 4:
                mu0_v4 = lt_muon_sel[0][0]
                mu1_v4 = lt_muon_sel[1][0]
                mu2_v4 = lt_muon_sel[2][0]
                mu3_v4 = lt_muon_sel[3][0]

                if self.get_muoncharge(lt_muon_sel[0][1])*self.get_muoncharge(lt_muon_sel[1][1]) < 0:
                    mz11 = (mu0_v4 + mu1_v4).M()
                    mz12 = (mu2_v4 + mu3_v4).M()

                if self.get_muoncharge(lt_muon_sel[0][1])*self.get_muoncharge(lt_muon_sel[2][1]) < 0:
                    mz21 = (mu0_v4 + mu2_v4).M()
                    mz22 = (mu1_v4 + mu3_v4).M()

                if self.get_muoncharge(lt_muon_sel[0][1])*self.get_muoncharge(lt_muon_sel[3][1]) < 0:
                    mz31 = (mu0_v4 + mu3_v4).M()
                    mz32 = (mu1_v4 + mu2_v4).M()

                dl1 = np.sqrt((self.Z_MASS - mz11)**2 + (self.Z_MASS - mz12)**2)
                dl2 = np.sqrt((self.Z_MASS - mz21)**2 + (self.Z_MASS - mz22)**2)
                dl3 = np.sqrt((self.Z_MASS - mz31)**2 + (self.Z_MASS - mz32)**2)

                mumu1_v4, mumu2_v4, lt_z1, lt_z2 = lep_pair(dl1, dl2, dl3, mu0_v4, mu1_v4, mu2_v4, mu3_v4)
            else:
                continue

            self.fill_cut('4 muons')

            mothers = None
            associated = None
            daughters = Mela.SimpleParticleCollection_t(pdgid, daughtersPt, daughtersEta, daughtersPhi, daughtersMass, True)
            self.mela.ghz1 = [1, 0]
            self.mela.setProcess(Mela.Process.HSMHiggs, Mela.MatrixElement.JHUGen, Mela.Production.ZZGG)
            self.mela.setInputEvent(daughters, associated, mothers, True)
            prob = self.mela.computeP(False)

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
            self.outlf['mumu1_inv_mass'][0] = mumu1_v4.M()
            self.outlf['mumu2_inv_mass'][0] = mumu2_v4.M()
            self.outlf['mumu1_pt'][0] = mumu1_v4.Pt()
            self.outlf['mumu2_pt'][0] = mumu2_v4.Pt()
            self.outlf['delta_mumu1_eta'][0] = abs(lt_z1[0][0].Eta()-lt_z1[1][0].Eta())
            self.outlf['delta_mumu2_eta'][0] = abs(lt_z2[0][0].Eta()-lt_z2[1][0].Eta())
            self.outlf['delta_mumu1_phi'][0] = abs(lt_z1[0][0].Phi()-lt_z1[1][0].Phi())
            self.outlf['delta_mumu2_phi'][0] = abs(lt_z2[0][0].Phi()-lt_z2[1][0].Phi())

            self.outlf['prob'][0] = prob

            genweight = self.br_event.At(0)
            self.outlf['weight'][0] = evt_weight * genweight.Weight
            self.outlf['dsid'][0] = int(self.procid)

            self.outtree.Fill()

    def end(self):
        super().end()
