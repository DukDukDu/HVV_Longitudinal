import ROOT as R
from util import lep_pair
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools
import numpy as np
#import Mela

class analysis_gg4e(analysis):
    #mela = Mela.Mela(13, 125, Mela.VerbosityLevel.SILENT)

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

    def get_echarge(self, idx):
        return self.br_electron.At(idx).Charge

    def cal_phi(self, l1_pt4, l2_pt4):
        delta_phi = 0
        if abs(l1_pt4.Phi()-l2_pt4.Phi()) < np.pi:
            delta_phi = abs(l1_pt4.Phi()-l2_pt4.Phi())
        else :
            delta_phi = 2*np.pi - abs(l1_pt4.Phi()-l2_pt4.Phi())

        return delta_phi
    
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

            pvector11, pvector11p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector12, pvector12p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector21, pvector21p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector22, pvector22p = np.array([0, 0, 0]), np.array([0, 0, 0])

            self.count_rawnb +=1

            for _ie in range(0, self.br_electron.GetEntries()):
                _e = self.br_electron.At(_ie)
                if _e.PT > 7 and abs(_e.Eta) < 2.5: #detector acceptance
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

                ee1_v4, ee2_v4, lt_z1, lt_z2 = lep_pair(dl1, dl2, dl3, lt_electron_sel)

                b_e11 = lt_z1[0][0].Clone(), b_e12 = lt_z1[1][0].Clone()
                b_e21 = lt_z2[0][0].Clone(), b_e22 = lt_z2[1][0].Clone()
                
                ee_t3_1 = ee1_v4.BoostVector()
                ee_t3_1 = R.TVector3(-ee_t3_1.X(), -ee_t3_1.Y(), -ee_t3_1.Z())
                b_e11.Boost(ee_t3_1)
                b_e12.Boost(ee_t3_1)

                ee_t3_2 = ee2_v4.BoostVector()
                ee_t3_2 = R.TVector3(-ee_t3_2.X(), -ee_t3_2.Y(), -ee_t3_2.Z())
                b_e21.Boost(ee_t3_2)
                b_e22.Boost(ee_t3_2)

                if self.get_echarge(lt_z1[0][1]) > 0:
                    pvector11 = np.array([b_e11.Px(), b_e11.Py(), b_e11.Pz()])
                    pvector12 = np.array([b_e12.Px(), b_e12.Py(), b_e12.Pz()])
                    pvector11p = np.array([lt_z1[0][0].Px(), lt_z1[0][0].Py(), lt_z1[0][0].Pz()])
                    pvector12p = np.array([lt_z1[1][0].Px(), lt_z1[1][0].Py(), lt_z1[1][0].Pz()])

                else:
                    pvector11 = np.array([b_e12.Px(), b_e12.Py(), b_e12.Pz()])
                    pvector12 = np.array([b_e11.Px(), b_e11.Py(), b_e11.Pz()])
                    pvector11p = np.array([lt_z1[1][0].Px(), lt_z1[1][0].Py(), lt_z1[1][0].Pz()])
                    pvector12p = np.array([lt_z1[0][0].Px(), lt_z1[0][0].Py(), lt_z1[0][0].Pz()])

                if self.get_echarge(lt_z2[0][1]) > 0:
                    pvector21 = np.array([b_e21.Px(), b_e21.Py(), b_e21.Pz()])
                    pvector22 = np.array([b_e22.Px(), b_e22.Py(), b_e22.Pz()])
                    pvector21p = np.array([lt_z2[0][0].Px(), lt_z2[0][0].Py(), lt_z2[0][0].Pz()])
                    pvector22p = np.array([lt_z2[1][0].Px(), lt_z2[1][0].Py(), lt_z2[1][0].Pz()])

                else:
                    pvector21 = np.array([b_e22.Px(), b_e22.Py(), b_e22.Pz()])
                    pvector22 = np.array([b_e21.Px(), b_e21.Py(), b_e21.Pz()])
                    pvector21p = np.array([lt_z2[1][0].Px(), lt_z2[1][0].Py(), lt_z2[1][0].Pz()])
                    pvector22p = np.array([lt_z2[0][0].Px(), lt_z2[0][0].Py(), lt_z2[0][0].Pz()])

                pvector1 = np.array([ee1_v4.Px(), ee1_v4.Py(), ee1_v4.Pz()])
                pvector2 = np.array([ee2_v4.Px(), ee2_v4.Py(), ee2_v4.Pz()])

            else:
                continue

            analysis.fill_cut(self, '4 electrons')

            pt_20_count = 0
            pt_10_count = 0
            #pt requirement
            if len(lt_electron_sel) == 4:
                for i in range(4):
                    if lt_electron_sel[i][0].Pt() > 20:
                        pt_20_count += 1
                    if lt_electron_sel[i][0].Pt() > 10:
                        pt_10_count += 1

                if pt_10_count >= 2 and pt_20_count >= 1:
                    pass
                else:
                    continue
            else:
                continue
            
            analysis.fill_cut(self, 'At least 2 leptons with pt > 10GeV and at least 1 lepton with pt > 20GeV')

            #ll' invariant mass requirement
            if len(lt_electron_sel) == 4:
                for i in range(4):
                    for j in range(i+1, 4):
                        if self.get_echarge(lt_electron_sel[i][1])*self.get_echarge(lt_electron_sel[j][1]) < 0:
                            if (lt_electron_sel[i][0] + lt_electron_sel[j][0]).Pt() > 4:
                                pass
                            else:
                                continue
            else:
                continue
            
            analysis.fill_cut(self, 'ml_1l_2 > 4GeV')

            tot_v4 = e0_v4 + e1_v4 + e2_v4 + e3_v4

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
            self.outlf['delta_ee1_phi'][0] = self.cal_phi(lt_z1[0][0], lt_z1[1][0])
            self.outlf['delta_ee2_phi'][0] = self.cal_phi(lt_z2[0][0], lt_z2[1][0])

            self.outlf['probsig'][0] = 0#probsig
            self.outlf['probbkg'][0] = 0#probbkg
            self.outlf['D_value'][0] = 0#probsig/(probbkg+probsig)

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
        analysis.end(self)
