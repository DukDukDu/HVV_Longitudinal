import ROOT as R
from util import lep_pair
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools
#import Mela
import numpy as np

class analysis_gg4m(analysis):
    #mela = Mela.Mela(13, 125, Mela.VerbosityLevel.SILENT)

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
        
        analysis.mknewlf(self, 'inv_mass', 'F')
        analysis.mknewlf(self, 'mumu1_inv_mass', 'F')
        analysis.mknewlf(self, 'mumu2_inv_mass', 'F')
        analysis.mknewlf(self, 'mumu1_pt', 'F')
        analysis.mknewlf(self, 'mumu2_pt', 'F')
        analysis.mknewlf(self, 'delta_mumu1_eta', 'F')
        analysis.mknewlf(self, 'delta_mumu2_eta', 'F')
        analysis.mknewlf(self, 'delta_mumu1_phi', 'F')
        analysis.mknewlf(self, 'delta_mumu2_phi', 'F')

        analysis.mknewlf(self, 'probsig', 'F')
        analysis.mknewlf(self, 'probbkg', 'F')
        analysis.mknewlf(self, 'D_value', 'F')

        analysis.mknewlf( self, 'costheta1', 'F')
        analysis.mknewlf( self, 'costheta2', 'F')
        analysis.mknewlf( self, 'sintheta1', 'F')
        analysis.mknewlf( self, 'sintheta2', 'F')
        analysis.mknewlf( self, 'sinphi1', 'F')
        analysis.mknewlf( self, 'sinphi2', 'F')
        analysis.mknewlf( self, 'cosphi1', 'F')
        analysis.mknewlf( self, 'cosphi2', 'F')
        analysis.mknewlf( self, 'phi1', 'F')
        analysis.mknewlf( self, 'phi2', 'F')
        analysis.mknewlf( self, 'theta1', 'F')
        analysis.mknewlf( self, 'theta2', 'F')

    def get_muoncharge(self, idx):
        return self.br_muon.At(idx).Charge

    def cal_phi(self, l1_pt4, l2_pt4):
        delta_phi = 0
        if abs(l1_pt4.Phi()-l2_pt4.Phi()) < np.pi:
            delta_phi = abs(l1_pt4.Phi()-l2_pt4.Phi())
        else :
            delta_phi = 2*np.pi - abs(l1_pt4.Phi()-l2_pt4.Phi())

        return delta_phi

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

            pvector11, pvector11p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector12, pvector12p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector21, pvector21p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector22, pvector22p = np.array([0, 0, 0]), np.array([0, 0, 0])

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

                mumu1_v4, mumu2_v4, lt_z1, lt_z2 = lep_pair(dl1, dl2, dl3, lt_muon_sel)

                b_m11 = lt_z1[0][0].Clone(), b_m12 = lt_z1[1][0].Clone()
                b_m21 = lt_z2[0][0].Clone(), b_m22 = lt_z2[1][0].Clone()

                mm_t3_1 = mumu1_v4.BoostVector()
                mm_t3_1 = R.TVector3(-mm_t3_1.X(), -mm_t3_1.Y(), -mm_t3_1.Z())
                b_m11.Boost(mm_t3_1)
                b_m12.Boost(mm_t3_1)

                mm_t3_2 = mumu2_v4.BoostVector()
                mm_t3_2 = R.TVector3(-mm_t3_2.X(), -mm_t3_2.Y(), -mm_t3_2.Z())
                b_m21.Boost(mm_t3_2)
                b_m22.Boost(mm_t3_2)

                if self.get_echarge(lt_z1[0][1]) > 0:
                    pvector11 = np.array([b_m11.Px(), b_m11.Py(), b_m11.Pz()])
                    pvector12 = np.array([b_m12.Px(), b_m12.Py(), b_m12.Pz()])
                    pvector11p = np.array([lt_z1[0][0].Px(), lt_z1[0][0].Py(), lt_z1[0][0].Pz()])
                    pvector12p = np.array([lt_z1[1][0].Px(), lt_z1[1][0].Py(), lt_z1[1][0].Pz()])

                else:
                    pvector11 = np.array([b_m12.Px(), b_m12.Py(), b_m12.Pz()])
                    pvector12 = np.array([b_m11.Px(), b_m11.Py(), b_m11.Pz()])
                    pvector11p = np.array([lt_z1[1][0].Px(), lt_z1[1][0].Py(), lt_z1[1][0].Pz()])
                    pvector12p = np.array([lt_z1[0][0].Px(), lt_z1[0][0].Py(), lt_z1[0][0].Pz()])

                if self.get_echarge(lt_z2[0][1]) > 0:
                    pvector21 = np.array([b_m21.Px(), b_m21.Py(), b_m21.Pz()])
                    pvector22 = np.array([b_m22.Px(), b_m22.Py(), b_m22.Pz()])
                    pvector21p = np.array([lt_z2[0][0].Px(), lt_z2[0][0].Py(), lt_z2[0][0].Pz()])
                    pvector22p = np.array([lt_z2[1][0].Px(), lt_z2[1][0].Py(), lt_z2[1][0].Pz()])

                else:
                    pvector21 = np.array([b_m22.Px(), b_m22.Py(), b_m22.Pz()])
                    pvector22 = np.array([b_m21.Px(), b_m21.Py(), b_m21.Pz()])
                    pvector21p = np.array([lt_z2[1][0].Px(), lt_z2[1][0].Py(), lt_z2[1][0].Pz()])
                    pvector22p = np.array([lt_z2[0][0].Px(), lt_z2[0][0].Py(), lt_z2[0][0].Pz()])

                pvector1 = np.array([mumu1_v4.Px(), mumu1_v4.Py(), mumu1_v4.Pz()])
                pvector2 = np.array([mumu2_v4.Px(), mumu2_v4.Py(), mumu2_v4.Pz()])
            else:
                continue

            analysis.fill_cut(self, '4 muons')
            pt_20_count = 0
            pt_10_count = 0
            #pt requirement
            if len(lt_muon_sel) == 4:
                for i in range(4):
                    if lt_muon_sel[i][0].Pt() > 20:
                        pt_20_count += 1
                    if lt_muon_sel[i][0].Pt() > 10:
                        pt_10_count += 1

                if pt_10_count >= 2 and pt_20_count >= 1:
                    pass
                else:
                    continue
            else:
                continue
            
            analysis.fill_cut(self, 'At least 2 leptons with pt > 10GeV and at least 1 lepton with pt > 20GeV')

            #ll' invariant mass requirement
            if len(lt_muon_sel) == 4:
                for i in range(4):
                    for j in range(i+1, 4):
                        if self.get_muoncharge(lt_muon_sel[i][1])*self.get_muoncharge(lt_muon_sel[j][1]) < 0:
                            if (lt_muon_sel[i][0] + lt_muon_sel[j][0]).Pt() > 4:
                                pass
                            else:
                                continue
            else:
                continue
            
            analysis.fill_cut(self, 'ml_1l_2 > 4GeV')

            tot_v4 = mu0_v4 + mu1_v4 + mu2_v4 + mu3_v4

            if tot_v4.M() > 220:
                pass
            else:
                continue

            analysis.fill_cut(self, 'inv mass > 220 GeV')

            # mothers = None
            # associated = None
            # daughters = Mela.SimpleParticleCollection_t(pdgid, daughtersPt, daughtersEta, daughtersPhi, daughtersMass, True)
           
            # self.mela.setInputEvent(daughters, associated, mothers, True)
            # self.mela.setProcess(Mela.Process.HSMHiggs, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            # probsig = self.mela.computeP(False)

            # self.mela.setProcess(Mela.Process.bkgZZ, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            # probbkg = self.mela.computeP(False)

            costheta1 = - np.dot(pvector2, pvector11)/(np.linalg.norm(pvector2)*np.linalg.norm(pvector11))
            costheta2 = - np.dot(pvector1, pvector21)/(np.linalg.norm(pvector1)*np.linalg.norm(pvector21))

            sintheta1 = np.sqrt(1-costheta1**2)
            sintheta2 = np.sqrt(1-costheta2**2)

            theta1 = np.arccos(costheta1)/np.pi
            theta2 = np.arccos(costheta2)/np.pi
            
            cosphi1 = np.dot(np.cross(pgulon, pvector1), np.cross(pvector12p, pvector11p))/ \
                      (np.linalg.norm(np.cross(pgulon, pvector1))*np.linalg.norm(np.cross(pvector12p, pvector11p)))

            cosphi2 = -np.dot(np.cross(pgulon, pvector2), np.cross(pvector22p, pvector21p))/ \
                      (np.linalg.norm(np.cross(pgulon, pvector2))*np.linalg.norm(np.cross(pvector22p, pvector21p)))

            sinphi1, sinphi2 = 0, 0
            phi1, phi2 = 0, 0

            abssinphi1 = np.linalg.norm(np.cross(np.cross(pgulon, pvector1), np.cross(pvector12p, pvector11p)))/ \
                      (np.linalg.norm(np.cross(pgulon, pvector1))*np.linalg.norm(np.cross(pvector12p, pvector11p)))

            abssinphi2 = np.linalg.norm(np.cross(-np.cross(pgulon, pvector2), np.cross(pvector22p, pvector21p)))/ \
                      (np.linalg.norm(np.cross(pgulon, pvector2))*np.linalg.norm(np.cross(pvector22p, pvector21p)))

            if np.dot(np.cross(np.cross(pgulon, pvector1), np.cross(pvector12p, pvector11p)), pvector1) > 0:
                sinphi1 = abssinphi1
                phi1 = np.arccos(cosphi1)/np.pi
            else:
                sinphi1 = -abssinphi1
                phi1 = -np.arccos(cosphi1)/np.pi

            if np.dot(np.cross(-np.cross(pgulon, pvector2), np.cross(pvector22p, pvector21p)), pvector2) > 0:
                sinphi2 = abssinphi2
                phi2 = np.arccos(cosphi2)/np.pi
            else:
                sinphi2 = -abssinphi2
                phi2 = -np.arccos(cosphi2)/np.pi

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
            self.outlf['delta_mumu1_phi'][0] = self.cal_phi(lt_z1[0][0], lt_z1[1][0])
            self.outlf['delta_mumu2_phi'][0] = self.cal_phi(lt_z2[0][0], lt_z2[1][0])

            self.outlf['probsig'][0] = 0#probsig
            self.outlf['probbkg'][0] = 0#probbkg
            self.outlf['D_value'][0] = 0#probsig/(probbkg + probsig)

            self.outlf['costheta1'][0] = costheta1
            self.outlf['costheta2'][0] = costheta2
            self.outlf['sintheta1'][0] = sintheta1
            self.outlf['sintheta2'][0] = sintheta2
            self.outlf['cosphi1'][0] = cosphi1
            self.outlf['cosphi2'][0] = cosphi2
            self.outlf['sinphi1'][0] = sinphi1
            self.outlf['sinphi2'][0] = sinphi2
            self.outlf['phi1'][0] = phi1
            self.outlf['phi2'][0] = phi2
            self.outlf['theta1'][0] = theta1
            self.outlf['theta2'][0] = theta2

            genweight = self.br_event.At(0)
            self.outlf['weight'][0] = evt_weight * genweight.Weight
            self.outlf['dsid'][0] = int(self.procid)

            self.outtree.Fill()

    def end(self):
        super().end()
