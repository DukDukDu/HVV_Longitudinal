#include "string.h"
/////////////////////////////////////////////gg4l,from LHE file read
namespace LHE_4l{
void Fill_histogram(TFile *file, TH1F *inv_mass, TH1F *leadingpT, TH1F *eeinv){
    TTree *tree = (TTree*)file->Get("LHEF");
    
    int pid[10], n;
    double px[10], py[10], pz[10], E[10];
    double pT[10], eta[10], phi[10];
    int moth1[10],moth2[10];
    float Mass;
    TLorentzVector mom, mom_ee;

    tree->SetBranchAddress("Particle.Px", &px);
    tree->SetBranchAddress("Particle.Py", &py);
    tree->SetBranchAddress("Particle.Pz", &pz);
    tree->SetBranchAddress("Particle.E", &E);
    tree->SetBranchAddress("Particle.PID", &pid);
    tree->SetBranchAddress("Particle.PT", &pT);
    tree->SetBranchAddress("Particle.Mother1", &moth1);
    tree->SetBranchAddress("Particle.Mother2", &moth2);
    tree->SetBranchAddress("inv_mass", &Mass);
    tree->SetBranchAddress("Particle.Eta", &eta);
    tree->SetBranchAddress("Particle.Phi", &phi);

    n = tree->GetEntries();
    cout << n << endl;
    double count_z_number=0;

    for (int i = 0; i < n; i++){
        tree->GetEntry(i);
        double px_l=0, py_l=0, pz_l=0, E_l=0, eta_l=0, phi_l=0, pT_l=0;
        double px_ee=0, py_ee=0, pz_ee=0, pt_ee=0, E_ee=0;
        double delta_eta=0, delta_eta_tem=0;
        double delta_phi=0, delta_phi_tem=0;
        double leading_pT=0, leading_pT_tem=0;
        bool have_Z = false;
        
        if(Mass > 150.){

            for (int j = 0; j < 10; j++){
                //calculate inviriant mass
                if(pid[j] == 11 || pid[j] == -11 || pid[j] == 13 || pid [j] == -13){

                    px_l = px_l + px[j];
                    py_l = py_l + py[j];
                    pz_l = pz_l + pz[j];
                    E_l = E_l +E[j];
                
                // leading_pT = pT[j];
                // if (leading_pT_tem >= pT[j]) leading_pT = leading_pT_tem;//calculate leading pT
                // leading_pT_tem = leading_pT;

                // delta_eta = eta[j] - delta_eta_tem;//calculate delta eta
                // delta_eta_tem = eta[j];

                // delta_phi = phi[j] - delta_phi_tem;//calculate delta phi
                // delta_phi_tem = phi[j];

            }

                if(pid[j] == 23) {

                    leading_pT = pT[j];
                    if (leading_pT_tem > pT[j]) leading_pT = leading_pT_tem;//calculate leading pT
                    leading_pT_tem = leading_pT;
                    have_Z = true;
                //leadingpT->Fill(pT[j]);
            }
                if(pid[j] == 11){

                    for(int j1 = 0; j1 < 10 ; j1++){//find electron pairs

                        if(pid[j1] == -11 && moth1[j] == moth1[j1] && moth1[j] != 0){
                            px_ee = px[j] + px[j1];
                            py_ee = py[j] + py[j1];
                            pz_ee = pz[j] + pz[j1];
                            E_ee = E[j] + E[j1];
                            pt_ee = sqrt(px_ee*px_ee + py_ee*py_ee);
                            leadingpT->Fill(pt_ee);
                            mom_ee.SetPxPyPzE(px_ee, py_ee, pz_ee, E_ee);
                            eeinv->Fill(mom_ee.M());
                    }
                }
            }

        }

        }
        //set all array elements 0 to avoid mixing with next event
        memset(pz, 0, sizeof(pz)), memset(px, 0, sizeof(px)), memset(py, 0, sizeof(py));
        memset(E, 0, sizeof(E)), memset(pT, 0, sizeof(pT));
        memset(pid, 0, sizeof(pid)),memset(eta, 0, sizeof(eta)), memset(phi, 0, sizeof(phi));
        memset(moth1, 0, sizeof(moth1)),memset(moth2, 0, sizeof(moth2));
        
        mom.SetPxPyPzE(px_l, py_l, pz_l, E_l);//calculate inv mass

        //Fill Histgram
        //if(mom.M()>180) 
        if(mom.M() != 0) inv_mass->Fill(mom.M());                    
        //if(have_Z) leadingpT->Fill(leading_pT);
        // deltaeta->Fill(abs(delta_eta));
        // deltaphi->Fill(abs(delta_phi));
    }

}
}