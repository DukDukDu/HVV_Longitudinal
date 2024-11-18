#include "string.h"
#include "math.h"
/////////////////////////////////////////////ggzz,from LHE file read
namespace LHE{
void Fill_histogram(TFile *file){
    TTree *tree = (TTree*)file->Get("LHEF");
    TFile *ana = new TFile("./anazz.root", "RECREATE");
    TTree *outputTree = new TTree("Var", "A new tree");
    
    int pid[4], n;
    double px[4], py[4], pz[4], E[4];
    double pT[4], eta[4], phi[4];
    double absdelta_eta=0, absdelta_phi=0, fleading_pT=0, inv_mass=0;
    TLorentzVector mom;

    tree->SetBranchAddress("Particle.Px", &px);
    tree->SetBranchAddress("Particle.Py", &py);
    tree->SetBranchAddress("Particle.Pz", &pz);
    tree->SetBranchAddress("Particle.E", &E);
    tree->SetBranchAddress("Particle.PID", &pid);
    tree->SetBranchAddress("Particle.PT", &pT);
    tree->SetBranchAddress("Particle.Eta", &eta);
    tree->SetBranchAddress("Particle.Phi", &phi);

    outputTree->Branch("absdelta_eta", &absdelta_eta, "absdelta_eta/D");
    outputTree->Branch("absdelta_phi", &absdelta_phi, "absdelta_phi/D");
    outputTree->Branch("leading_pT", &fleading_pT, "leading_pT/D");
    outputTree->Branch("inv_mass", &inv_mass, "inv_mass/D");

    n = tree->GetEntries();
    cout << n << endl;

    for (int i = 0; i < n; i++){
        tree->GetEntry(i);
        double px_l=0, py_l=0, pz_l=0, E_l=0, eta_l=0, phi_l=0, pT_l=0;
        double delta_eta_tem=0;
        double delta_phi_tem=0;
        double leading_pT_tem=0;
        double delta_eta=0, delta_phi=0, leading_pT=0;
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
        inv_mass = mom.M();
        //cout << mom.M() << endl;

        if(abs(delta_phi) > M_PI){
            absdelta_phi = 2*M_PI - abs(delta_phi);
        }
        else absdelta_phi = abs(delta_phi);

        //cout << absdelta_phi << endl;

        absdelta_eta = abs(delta_eta);
        fleading_pT = leading_pT;
        //cout << absdelta_eta << endl;

        outputTree->Fill();
    }
    outputTree->Write();

    file->Close();
    ana->Close();
}
}