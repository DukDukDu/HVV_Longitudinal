import ROOT as R
from array import array
import anaconfig
import sampleconfig_lhe
from analysis_lhe import analysis
import math
import itertools
import Mela 
import numpy as np

class analysis_gg2e2m(analysis):
    mela = Mela.Mela(13, 125, Mela.VerbosityLevel.SILENT)   #Mela initialization
    def __init__(self, ch, sampleID, nevent, basic_weight, outfnm):
        analysis.__init__(self, ch, sampleID, nevent, basic_weight, outfnm)
        self.MUON_MASS = 0.1056583755  # PDG 2023 MOHR
        self.ELE_MASS = 0.00051099895000 # PDG 2023 MOHR

    def begin(self):
        analysis.begin(self)
        analysis.mknewlf(self, 'eeinv', 'F')
        analysis.mknewlf(self, 'mminv', 'F')
        analysis.mknewlf(self, 'inv_mass', 'F')
        analysis.mknewlf(self, 'leading_l_eta', 'F')
        analysis.mknewlf(self, 'leading_z_eta', 'F')
        analysis.mknewlf(self, 'leadingpT_z', 'F')
        analysis.mknewlf(self, 'leadingpT_l', 'F')
        analysis.mknewlf(self, 'probsig', 'F')
        analysis.mknewlf(self, 'probbkg', 'F')
        analysis.mknewlf(self, 'probbkg_qq', 'F')

    def loop(self):
        for i in range(0, self.nevt):
            self.reader.ReadEntry(i)
            analysis.fill_cut(self, 'NO CUT')

            analysis.fill_dummy(self)

            daughtersPt = []
            daughtersEta = []
            daughtersPhi = []
            daughtersMass = []
            pdgid = []
            l_arr = []
            z_arr = []
            mom = None
            mom_ee = None
            mom_mm = None
            have_l = 0
            have_z = 0
            leading_pT_tem_l =0
            leading_pT_l = 0
            mom_px = 0
            mom_py = 0
            mom_pz = 0
            mom_E = 0
            mom_ee_px = 0
            mom_ee_py = 0
            mom_ee_pz = 0
            mom_ee_E = 0
            mom_mm_px = 0
            mom_mm_py = 0
            mom_mm_pz = 0
            mom_mm_E = 0

            self.count_rawnb +=1

            for _i_par in range(0, self.br_particle.GetEntries()):
                _p = self.br_particle.At(_i_par)
                if _p.PID == 11 or _p.PID == -11 or _p.PID == 13 or _p.PID == -13:
                    have_l += 1
                    mom_px += _p.Px
                    mom_py += _p.Py
                    mom_pz += _p.Pz
                    mom_E += _p.E 

                    l_arr.append((_p.PT, _p.Eta))

                if _p.PID == 11 or _p.PID == -11:
                    mom_ee_px += _p.Px
                    mom_ee_py += _p.Py
                    mom_ee_pz += _p.Pz
                    mom_ee_E += _p.E 
                    pdgid.append(_p.PID)
                    daughtersPt.append(_p.PT), daughtersPhi.append(_p.Phi)
                    daughtersEta.append(_p.Eta), daughtersMass.append(self.ELE_MASS)

                if _p.PID == 13 or _p.PID == -13:
                    mom_mm_px += _p.Px
                    mom_mm_py += _p.Py
                    mom_mm_pz += _p.Pz
                    mom_mm_E += _p.E
                    pdgid.append(_p.PID)
                    daughtersPt.append(_p.PT), daughtersPhi.append(_p.Phi)
                    daughtersEta.append(_p.Eta), daughtersMass.append(self.MUON_MASS)

            analysis.sort_pt(self, l_arr)
            mom = R.TLorentzVector(mom_px, mom_py, mom_pz, mom_E)
            mom_ee = R.TLorentzVector(mom_ee_px, mom_ee_py, mom_ee_pz, mom_ee_E)
            mom_mm = R.TLorentzVector(mom_mm_px, mom_mm_py, mom_mm_pz, mom_mm_E)

            z_arr.append((mom_ee.Pt(), mom_ee.Eta()))
            z_arr.append((mom_mm.Pt(), mom_mm.Eta()))
            analysis.sort_pt(self, z_arr)

            daughters = Mela.SimpleParticleCollection_t(pdgid, daughtersPt, daughtersEta, daughtersPhi, daughtersMass, True)
            mothers = None
            associated = None

            self.mela.setInputEvent(daughters, associated, mothers, True)

            self.mela.setProcess(Mela.Process.HSMHiggs, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            probsig = self.mela.computeP(False)
            
            self.mela.setProcess(Mela.Process.bkgZZ, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            probbkg = self.mela.computeP(False)
            
            self.mela.setProcess(Mela.Process.bkgZZ, Mela.MatrixElement.MCFM, Mela.Production.ZZQQB)
            probbkg_qq = self.mela.computeP(False)

            self.mela.setProcess(Mela.Process.bkgZZ_SMHiggs, Mela.MatrixElement.MCFM, Mela.Production.ZZGG)
            probtot = self.mela.computeP(False)


            self.outlf['eeinv'][0] =mom_ee.M()
            self.outlf['mminv'][0] =mom_mm.M()
            self.outlf['inv_mass'][0] =mom.M()
            self.outlf['leading_l_eta'][0] =l_arr[0][1]
            self.outlf['leading_z_eta'][0] =z_arr[0][1]
            self.outlf['leadingpT_z'][0] =z_arr[0][0]
            self.outlf['leadingpT_l'][0] =l_arr[0][0]
            self.outlf['probsig'][0] =probsig
            self.outlf['probbkg'][0] =probbkg
            self.outlf['probbkg_qq'][0] =probbkg_qq
            self.outlf['weight'][0] =0
            self.outlf['dsid'][0] =0

            self.outtree.Fill()


    def end(self):
        analysis.end(self)



                    
