import ROOT as R
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools
#import Mela 
import numpy as np

class analysis_gg2e2m(analysis):
    #mela = Mela.Mela(13, 125, Mela.VerbosityLevel.SILENT)   #Mela initialization

    def __init__(self, ch, sampleID, nevent, basic_weight, outfnm):
        analysis.__init__(self, ch, sampleID, nevent, basic_weight, outfnm)
        self.MUON_MASS = 0.1056583755  # PDG 2023 MOHR
        self.ELE_MASS = 0.00051099895000 # PDG 2023 MOHR

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

        analysis.mknewlf( self, 'inv_mass', 'F')
        analysis.mknewlf( self, 'ee_inv_mass', 'F')
        analysis.mknewlf( self, 'mm_inv_mass', 'F')
        analysis.mknewlf( self, 'ee_pt', 'F')
        analysis.mknewlf( self, 'mm_pt', 'F')
        analysis.mknewlf( self, 'delta_eta_e', 'F')
        analysis.mknewlf( self, 'delta_eta_m', 'F')
        analysis.mknewlf( self, 'delta_phi_e', 'F')
        analysis.mknewlf( self, 'delta_phi_m', 'F')

        analysis.mknewlf( self, 'probsig', 'F')
        analysis.mknewlf( self, 'probbkg', 'F')
        analysis.mknewlf( self, 'D_value', 'F')

        analysis.mknewlf( self, 'theta_cos1cos2', 'F')
        analysis.mknewlf( self, 'phi_cos1cos2', 'F')
        analysis.mknewlf( self, 'phi_sin1sin2', 'F')
        analysis.mknewlf( self, 'sinphi1costheta1', 'F')
        analysis.mknewlf( self, 'sinphi2costheta2', 'F')
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
            lt_muon_sel = []
            lepton_v4 = []
            pdgid = []
            daughtersPt = []
            daughtersEta = []
            daughtersPhi = []
            daughtersMass = []

            e0_v4, b_e0_v4 = None, None
            e1_v4, b_e1_v4 = None, None
            mu0_v4, b_mu0_v4 = None, None
            mu1_v4, b_mu1_v4 = None, None
            ee_v4 = None
            mm_v4 = None
            tot_v4 = None

            pvector11, pvector11p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector12, pvector12p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector21, pvector21p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pvector22, pvector22p = np.array([0, 0, 0]), np.array([0, 0, 0])
            pgulon = np.array([0, 0, 1])

            self.count_rawnb +=1

            for _ie in range(0, self.br_electron.GetEntries()):
                _e = self.br_electron.At(_ie)
                if _e.PT > 7 and abs(_e.Eta) < 2.5: # detector acceptance cut
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_e.PT, _e.Eta, _e.Phi, self.ELE_MASS)
                    lt_electron_sel.append((_v, _ie))
                    lepton_v4.append((_v, _ie))
                    daughtersPt.append(_e.PT), daughtersEta.append(_e.Eta)  #Save these for Mela calculation
                    daughtersPhi.append(_e.Phi), daughtersMass.append(self.ELE_MASS)
                    if self.get_echarge(_ie) > 0:
                        pdgid.append(-11)
                    else:
                        pdgid.append(11)

            analysis.sort_pt(self, lt_electron_sel)

            for _imu in range(0, self.br_muon.GetEntries()):
                _mu = self.br_muon.At(_imu)
                if _mu.PT > 5 and abs(_mu.Eta) < 2.4: # detector acceptance cut
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_mu.PT, _mu.Eta, _mu.Phi, self.MUON_MASS)
                    lt_muon_sel.append((_v, _imu))
                    lepton_v4.append((_v, _imu))
                    daughtersPt.append(_mu.PT), daughtersEta.append(_mu.Eta)
                    daughtersPhi.append(_mu.Phi), daughtersMass.append(self.MUON_MASS)
                    if self.get_muoncharge(_imu) > 0:
                        pdgid.append(-13)
                    else:
                        pdgid.append(13)

            analysis.sort_pt(self, lt_muon_sel)

            if len(lt_electron_sel) == 2:
                if self.get_echarge(lt_electron_sel[0][1])*self.get_echarge(lt_electron_sel[1][1]) < 0:
                    e0_v4 = lt_electron_sel[0][0]
                    b_e0_v4 = e0_v4.Clone()
                    e1_v4= lt_electron_sel[1][0]
                    b_e1_v4 = e1_v4.Clone()
                    ee_v4 = e0_v4 + e1_v4
                    ee_t3 = ee_v4.BoostVector()
                    ee_t3 = R.TVector3(-ee_t3.X(), -ee_t3.Y(), -ee_t3.Z())
                    #print(ee_t3.X())
                    #ee_t3 = R.TVector3(1, 1, 1)
                    b_e0_v4.Boost(ee_t3)
                    b_e1_v4.Boost(ee_t3)
                    #print(b_e0_v4.Px())
                    #print(e0_v4)
                    #print(lt_electron_sel)
                    if self.get_echarge(lt_electron_sel[0][1]) > 0:
                        pvector11 = np.array([b_e0_v4.Px(), b_e0_v4.Py(), b_e0_v4.Pz()])
                        pvector12 = np.array([b_e1_v4.Px(), b_e1_v4.Py(), b_e1_v4.Pz()])
                        pvector11p = np.array([e0_v4.Px(), e0_v4.Py(), e0_v4.Pz()])
                        pvector12p = np.array([e1_v4.Px(), e1_v4.Py(), e1_v4.Pz()])
                    else:
                        pvector11 = np.array([b_e1_v4.Px(), b_e1_v4.Py(), b_e1_v4.Pz()])
                        pvector12 = np.array([b_e0_v4.Px(), b_e0_v4.Py(), b_e0_v4.Pz()])
                        pvector11p = np.array([e1_v4.Px(), e1_v4.Py(), e1_v4.Pz()])
                        pvector12p = np.array([e0_v4.Px(), e0_v4.Py(), e0_v4.Pz()])
                else:
                    continue
            
            else:
                continue

            analysis.fill_cut(self, '2 oppo sign electron within detector acceptance')

            if len(lt_muon_sel) == 2:
                if self.get_muoncharge(lt_muon_sel[0][1])*self.get_muoncharge(lt_muon_sel[1][1]) < 0:
                    mu0_v4 = lt_muon_sel[0][0]
                    b_mu0_v4 = mu0_v4.Clone()
                    mu1_v4 = lt_muon_sel[1][0]
                    b_mu1_v4 = mu1_v4.Clone()
                    mm_v4 = mu0_v4 + mu1_v4
                    mm_t3 = mm_v4.BoostVector()
                    #print(mm_t3.X())
                    mm_t3 = R.TVector3(-mm_t3.X(), -mm_t3.Y(), -mm_t3.Z())
                    #print(mm_t3.X())
                    b_mu0_v4.Boost(mm_t3)
                    b_mu1_v4.Boost(mm_t3)
                    if self.get_muoncharge(lt_muon_sel[0][1]) > 0:
                        pvector21 = np.array([b_mu0_v4.Px(), b_mu0_v4.Py(), b_mu0_v4.Pz()])
                        pvector22 = np.array([b_mu1_v4.Px(), b_mu1_v4.Py(), b_mu1_v4.Pz()])
                        pvector21p = np.array([mu0_v4.Px(), mu0_v4.Py(), mu0_v4.Pz()])
                        pvector22p = np.array([mu1_v4.Px(), mu1_v4.Py(), mu1_v4.Pz()])
                    else:
                        pvector21 = np.array([b_mu1_v4.Px(), b_mu1_v4.Py(), b_mu1_v4.Pz()])
                        pvector22 = np.array([b_mu0_v4.Px(), b_mu0_v4.Py(), b_mu0_v4.Pz()])
                        pvector21p = np.array([mu1_v4.Px(), mu1_v4.Py(), mu1_v4.Pz()])
                        pvector22p = np.array([mu0_v4.Px(), mu0_v4.Py(), mu0_v4.Pz()])

                    #print(pvector21)
                else:
                    continue

            else:
                continue

            analysis.fill_cut(self, '2 oppo sign muon within detector acceptance')

            if (e0_v4 + e1_v4 + mu0_v4 + mu1_v4).M() > 220:
                pass
            else:
                continue

            analysis.fill_cut(self, 'm4l > 220GeV')

            pt_20_count = 0
            pt_10_count = 0
            
            #pt requirement 
            if len(lepton_v4) == 4: 
                for i in range(4):
                    if lepton_v4[i][0].Pt() >= 20:
                        pt_20_count +=1
                    if lepton_v4[i][0].Pt() >= 10:
                        pt_10_count +=1

                if pt_20_count >=1 and pt_10_count >=2:
                    pass
                else:
                    continue
            else:
                continue

            analysis.fill_cut(self, 'At least 2 leptons with pt > 10GeV and at least 1 lepton with pt > 20GeV')
            
            #ll' invariant mass requirement
            if len(lepton_v4) == 4:
                for i in range(2):
                    for j in range(i+1 ,4):
                        if j <=1:
                            if self.get_echarge(lepton_v4[i][1])*self.get_echarge(lepton_v4[j][1]) < 0: #a pair of electrons OC
                                if (lepton_v4[i][0] + lepton_v4[j][0]).Pt() > 4:
                                    pass
                                else:
                                    continue
                            else:
                                continue
                        else:
                            if self.get_echarge(lepton_v4[i][1])*self.get_muoncharge(lepton_v4[j][1]) < 0: #a pair of muon and electron OC
                                if (lepton_v4[i][0] + lepton_v4[j][0]).Pt() > 4:
                                    pass
                                else:
                                    continue
                if self.get_muoncharge(lepton_v4[2][1])*self.get_muoncharge(lepton_v4[3][1]) < 0: #a pair of muons OC
                    if (lepton_v4[2][0]+lepton_v4[3][0]).Pt() > 4:
                        pass
                    else:
                        continue
                else:
                    continue
            else:
                continue

            analysis.fill_cut(self, 'ml_1l_2 > 4GeV')

            # daughters = Mela.SimpleParticleCollection_t(pdgid, daughtersPt, daughtersEta, daughtersPhi, daughtersMass, True)
            # mothers = None
            # associated = None
            # # print(pdgid)
            # # print(daughtersPt)
            
            # #Mela calculating the probability assuming different processes
            # self.mela.setInputEvent(daughters, associated, mothers, True)
            
            # self.mela.setProcess(Mela.Process.HSMHiggs, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            # probsig = self.mela.computeP(False)
            
            # self.mela.setProcess(Mela.Process.bkgZZ, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            # probbkg = self.mela.computeP(False)
            
            #calculate the theta an phi angle
            tot_v4 = e0_v4 + e1_v4 + mu0_v4 + mu1_v4

            pvector1 = np.array([ee_v4.Px(), ee_v4.Py(), ee_v4.Pz()])
            pvector2 = np.array([mm_v4.Px(), mm_v4.Py(), mm_v4.Pz()])

            costheta1 = - np.dot(pvector2, pvector11)/(np.linalg.norm(pvector2)*np.linalg.norm(pvector11))
            costheta2 = - np.dot(pvector1, pvector21)/(np.linalg.norm(pvector1)*np.linalg.norm(pvector21))

            sintheta1 = np.sqrt(1-costheta1**2)
            sintheta2 = np.sqrt(1-costheta2**2)

            theta1 = np.arccos(costheta1)/np.pi
            theta2 = np.arccos(costheta2)/np.pi

            theta_cos1cos2 = costheta1*costheta2
            
            cosphi1 = np.dot(np.cross(pgulon, pvector1), np.cross(pvector12p, pvector11p))/ \
                      (np.linalg.norm(np.cross(pgulon, pvector1))*np.linalg.norm(np.cross(pvector12p, pvector11p)))

            cosphi2 = -np.dot(np.cross(pgulon, pvector2), np.cross(pvector22p, pvector21p))/ \
                      (np.linalg.norm(np.cross(pgulon, pvector2))*np.linalg.norm(np.cross(pvector22p, pvector21p)))

            phi_cos1cos2 = cosphi1*cosphi2

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

            phi_sin1sin2 = sinphi1*sinphi2

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

            self.outlf['inv_mass'][0] = tot_v4.M()
            self.outlf['ee_inv_mass'][0] = ee_v4.M()
            self.outlf['mm_inv_mass'][0] = mm_v4.M()
            self.outlf['ee_pt'][0] = ee_v4.Pt()
            self.outlf['mm_pt'][0] = mm_v4.Pt()
            self.outlf['delta_eta_e'][0] = abs(e0_v4.Eta() - e1_v4.Eta())
            self.outlf['delta_eta_m'][0] = abs(mu0_v4.Eta() - mu1_v4.Eta())
            self.outlf['delta_phi_e'][0] = self.cal_phi(e0_v4, e1_v4)
            self.outlf['delta_phi_m'][0] = self.cal_phi(mu0_v4, mu1_v4)

            self.outlf['probsig'][0] = 0#probsig
            self.outlf['probbkg'][0] = 0#probbkg
            self.outlf['D_value'][0] = 0#probsig/(probsig+probbkg)

            self.outlf['theta_cos1cos2'][0] = theta_cos1cos2
            self.outlf['phi_cos1cos2'][0] = phi_cos1cos2
            self.outlf['phi_sin1sin2'][0] = phi_sin1sin2
            self.outlf['sinphi1costheta1'][0] = sinphi1*costheta1
            self.outlf['sinphi2costheta2'][0] = sinphi2*costheta2
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
