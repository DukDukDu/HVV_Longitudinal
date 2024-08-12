import ROOT as R
from array import array
import anaconfig
import sampleconfig
from analysis import analysis
import math
import itertools
import Mela 

class analysis_gg2e2m(analysis):
    mela = Mela.Mela(13, 125, Mela.VerbosityLevel.SILENT)   #Mela initialization

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
            pdgid = []
            daughtersPt = []
            daughtersEta = []
            daughtersPhi = []
            daughtersMass = []

            e0_v4 = None
            e1_v4 = None
            mu0_v4 = None
            mu1_v4 = None
            ee_v4 = None
            mm_v4 = None
            tot_v4 = None

            self.count_rawnb +=1

            for _ie in range(0, self.br_electron.GetEntries()):
                _e = self.br_electron.At(_ie)
                if _e.PT > 7 and abs(_e.Eta) < 2.5:
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_e.PT, _e.Eta, _e.Phi, self.ELE_MASS)
                    lt_electron_sel.append((_v, _ie))
                    daughtersPt.append(_e.PT), daughtersEta.append(_e.Eta)  #Save these for Mela calculation
                    daughtersPhi.append(_e.Phi), daughtersMass.append(self.ELE_MASS)
                    if self.get_echarge(_ie) > 0:
                        pdgid.append(-11)
                    else:
                        pdgid.append(11)

            analysis.sort_pt(self, lt_electron_sel)

            for _imu in range(0, self.br_muon.GetEntries()):
                _mu = self.br_muon.At(_imu)
                if _mu.PT > 5 and abs(_mu.Eta) < 2.4:
                    _v = R.TLorentzVector()
                    _v.SetPtEtaPhiM(_mu.PT, _mu.Eta, _mu.Phi, self.MUON_MASS)
                    lt_muon_sel.append((_v, _imu))
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
                    e1_v4 = lt_electron_sel[1][0]
                    #print(lt_electron_sel)

                else:
                    continue
            
            else:
                continue

            analysis.fill_cut(self, '2 oppo sign electron')

            if len(lt_muon_sel) == 2:
                if self.get_muoncharge(lt_muon_sel[0][1])*self.get_muoncharge(lt_muon_sel[1][1]) < 0:
                    mu0_v4 = lt_muon_sel[0][0]
                    mu1_v4 = lt_muon_sel[1][0]
                else:
                    continue

            else:
                continue

            analysis.fill_cut(self, '2 oppo sign muon')
            
            daughters = Mela.SimpleParticleCollection_t(pdgid, daughtersPt, daughtersEta, daughtersPhi, daughtersMass, True)
            mothers = None
            associated = None
            # print(pdgid)
            # print(daughtersPt)
            
            #Mela calculating the probability assuming different processes
            self.mela.setInputEvent(daughters, associated, mothers, True)
            
            self.mela.setProcess(Mela.Process.HSMHiggs, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            probsig = self.mela.computeP(False)
            
            self.mela.setProcess(Mela.Process.bkgZZ, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            probbkg = self.mela.computeP(False)

            ee_v4 = e0_v4 + e1_v4
            mm_v4 = mu0_v4 + mu1_v4
            tot_v4 = e0_v4 + e1_v4 + mu0_v4 + mu1_v4

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
            self.outlf['delta_phi_e'][0] = abs(e0_v4.Phi() - e1_v4.Phi())
            self.outlf['delta_phi_m'][0] = abs(mu0_v4.Phi() - mu1_v4.Phi())

            self.outlf['probsig'][0] = probsig
            self.outlf['probbkg'][0] = probbkg
            self.outlf['D_value'][0] = probsig/(probsig+probbkg)

            genweight = self.br_event.At(0)
            self.outlf['weight'][0] = evt_weight * genweight.Weight
            self.outlf['dsid'][0] = int(self.procid)

            self.outtree.Fill()

    def end(self):
        analysis.end(self)
