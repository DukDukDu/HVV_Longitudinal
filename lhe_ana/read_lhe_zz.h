#include "string.h"
/////////////////////////////////////////////ggzz,from LHE file read
namespace LHE{
void Fill_histogram(TFile *file, TH1F *inv_mass, TH1F *leadingpt, TH1F *deltaeta, TH1F *deltaphi){
    TTree *tree = (TTree*)file->Get("LHEF");
    
    int pid[4], n;
    double px[4], py[4], pz[4], E[4];
    double pT[4], eta[4], phi[4];
    TLorentzVector mom;

    tree->SetBranchAddress("Particle.Px", &px);
    tree->SetBranchAddress("Particle.Py", &py);
    tree->SetBranchAddress("Particle.Pz", &pz);
    tree->SetBranchAddress("Particle.E", &E);
    tree->SetBranchAddress("Particle.PID", &pid);
    tree->SetBranchAddress("Particle.PT", &pT);
    tree->SetBranchAddress("Particle.Eta", &eta);
    tree->SetBranchAddress("Particle.Phi", &phi);

    n = tree->GetEntries();
    cout << n << endl;

    for (int i = 0; i < n; i++){
        tree->GetEntry(i);
        double px_l=0, py_l=0, pz_l=0, E_l=0, eta_l=0, phi_l=0, pT_l=0;
        double delta_eta=0, delta_eta_tem=0;
        double delta_phi=0, delta_phi_tem=0;
        double leading_pT=0, leading_pT_tem=0; 
        for (int j = 0; j < 4; j++){
            if(pid[j] == 23){
                px_l = px_l + px[j];
                py_l = py_l + py[j];
                pz_l = pz_l + pz[j];
                E_l = E_l +E[j];
                
                leading_pT = pT[j];
                if (leading_pT_tem >= pT[j]) leading_pT = leading_pT_tem;//calculate leading pT
                leading_pT_tem = leading_pT;

                delta_eta = eta[j] - delta_eta_tem;//calculate delta eta
                delta_eta_tem = eta[j];

                delta_phi = phi[j] - delta_phi_tem;//calculate delta phi
                delta_phi_tem = phi[j];

            }

            pid[j] = px[j] = py[j] = pz[j] = pT[j] = E[j] = eta[j] = phi[j] = 0;
        }

        mom.SetPxPyPzE(px_l, py_l, pz_l, E_l);

        cout << mom.M() << endl;

        //Fill Histgram
        inv_mass->Fill(mom.M());
        leadingpt->Fill(leading_pT);
        deltaeta->Fill(abs(delta_eta));
        deltaphi->Fill(abs(delta_phi));
    }
}
}