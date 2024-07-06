#include "string.h"
/////////////////////////////////////////////gg4l,from LHE file read
namespace LHE_4l{
void Fill_histogram(TFile *file, TH1F *inv_mass, TH1F *leadingpT_z, TH1F *leadingpT_l, \
                    TH1F *leading_z_eta, TH1F *leading_l_eta, TH1F *l_phi, TH1F *eeinv, TH1F *mminv){
    TTree *tree = (TTree*)file->Get("LHEF");
    
    int pid[10], n, count=0;
    double px[10], py[10], pz[10], E[10];
    double pT[10], eta[10], phi[10];
    int moth1[10],moth2[10];
    float Mass;
    TLorentzVector mom, mom_ee, mom_mm;

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
        double px_mm=0, py_mm=0, pz_mm=0, pt_mm=0, E_mm=0;
        double tot_phi=0;
        double leading_pT=0, leading_pT_tem=0, leading_pT_l=0, leading_pT_tem_l=0;
        int have_z = 0, have_l = 0;
        int leading_z_No=0, leading_l_No=0, leading_z_No_tem=0, leading_l_No_tem=0;
        
        if(Mass > 140.){
            count = count + 1;
            for (int j = 0; j < 10; j++){
                //calculate inviriant mass
                if(pid[j] == 11 || pid[j] == -11 || pid[j] == 13 || pid[j] == -13){
                    have_l = have_l + 1;//count lepton number

                    px_l = px_l + px[j];
                    py_l = py_l + py[j];
                    pz_l = pz_l + pz[j];
                    E_l = E_l + E[j];
                    tot_phi = tot_phi + phi[j];
                
                    leading_pT_l = pT[j];
                    leading_l_No = j;
                    if (leading_pT_tem_l >= pT[j]){
                        leading_pT_l = leading_pT_tem_l;//calculate leading pT
                        leading_l_No = leading_l_No_tem;
                    }
                    leading_pT_tem_l = leading_pT_l;
                    leading_l_No_tem = leading_l_No;

            }

                if(pid[j] == 23) {

                    have_z = have_z + 1;//count z number

                    leading_pT = pT[j];
                    leading_z_No = j;
                    if (leading_pT_tem > pT[j]){
                        leading_pT = leading_pT_tem;//calculate leading pT
                        leading_z_No = leading_z_No_tem;
                    }
                    leading_pT_tem = leading_pT;
                    leading_z_No_tem = leading_z_No;
            }
                if(pid[j] == 11){

                    for(int je = 0; je < 10 ; je++){//find electron pairs

                        if(pid[je] == -11 && moth1[j] == moth1[je] && pid[moth1[j]] == 23){//select electron pairs from z(maybe on-shell)
                            px_ee = px[j] + px[je];
                            py_ee = py[j] + py[je];
                            pz_ee = pz[j] + pz[je];
                            E_ee = E[j] + E[je];
                            mom_ee.SetPxPyPzE(px_ee, py_ee, pz_ee, E_ee);
                            eeinv->Fill(mom_ee.M());//ee pair invmass
                    }
                }
            }
                if(pid[j] == 13){

                    for(int jm = 0; jm < 10 ; jm++){//find muon pairs

                        if(pid[jm] == -13 && moth1[j] == moth1[jm] && pid[moth1[j]] == 23){//select muon pairs from z(maybe on-shell)
                            px_mm = px[j] + px[jm];
                            py_mm = py[j] + py[jm];
                            pz_mm = pz[j] + pz[jm];
                            E_mm = E[j] + E[jm];
                            mom_mm.SetPxPyPzE(px_mm, py_mm, pz_mm, E_mm);
                            mminv->Fill(mom_mm.M());//mumu pair invmass
                            //cout << mom_mm.M() << " ";
                    }
                }
            }

        }

        }
        
                
        mom.SetPxPyPzE(px_l, py_l, pz_l, E_l);//fill 4l Lorentz vec
        //cout << have_z << " ";
        //Fill Histgram                   
        if(have_z != 0){//choose 2 z event 
            leadingpT_z->Fill(leading_pT);
            leading_z_eta->Fill(eta[leading_z_No]);
        }
        if(have_l == 4){//final states must contain 4l
            leadingpT_l->Fill(leading_pT_l);
            leading_l_eta->Fill(eta[leading_l_No]);
            l_phi->Fill(tot_phi);
            inv_mass->Fill(mom.M()); 
        } 
        
        //set all array elements 0 to avoid mixing with next event
        memset(pz, 0, sizeof(pz)), memset(px, 0, sizeof(px)), memset(py, 0, sizeof(py));
        memset(E, 0, sizeof(E)), memset(pT, 0, sizeof(pT));
        memset(pid, 0, sizeof(pid)),memset(eta, 0, sizeof(eta)), memset(phi, 0, sizeof(phi));
        memset(moth1, 0, sizeof(moth1)),memset(moth2, 0, sizeof(moth2));
    }

    cout << count << endl;

}
}