#include "string.h"
/////////////////////////////////////////////gg4l,from LHE file read
namespace LHE_4l{
void Fill_histogram(TFile *file){
    TTree *tree = (TTree*)file->Get("LHEF");
    TFile *ana = new TFile("./ana4l.root", "RECREATE");
    TTree *outputTree = new TTree("Var", "A new tree");
    
    int pid[10], n, count=0;
    double px[10], py[10], pz[10], E[10];
    double pT[10], eta[10], phi[10];
    int moth1[10],moth2[10];
    double l_e_phi = 0, l_ep_phi = 0, l_mu_phi = 0, l_mup_phi = 0;
    TLorentzVector mom, mom_ee, mom_mm;
    double eeinv=0, mminv=0, inv_mass=0;
    double leading_l_eta=0, leading_z_eta=0, leadingpT_z=0, leadingpT_l=0;

    tree->SetBranchAddress("Particle.Px", &px);
    tree->SetBranchAddress("Particle.Py", &py);
    tree->SetBranchAddress("Particle.Pz", &pz);
    tree->SetBranchAddress("Particle.E", &E);
    tree->SetBranchAddress("Particle.PID", &pid);
    tree->SetBranchAddress("Particle.PT", &pT);
    tree->SetBranchAddress("Particle.Mother1", &moth1);
    tree->SetBranchAddress("Particle.Mother2", &moth2);
    tree->SetBranchAddress("Particle.Eta", &eta);
    tree->SetBranchAddress("Particle.Phi", &phi);

    //outputTree->Branch("l_phi", &l_phi, "l_phi/D");
    outputTree->Branch("eeinv", &eeinv, "eeinv/D");
    outputTree->Branch("mminv", &mminv, "mminv/D");
    outputTree->Branch("inv_mass", &inv_mass, "inv_mass/D");
    outputTree->Branch("leading_l_eta", &leading_l_eta, "leading_l_eta/D");
    outputTree->Branch("leading_z_eta", &leading_z_eta, "leading_z_eta/D");
    outputTree->Branch("leadingpT_z", &leadingpT_z, "leadingpT_z/D");
    outputTree->Branch("leadingpT_l", &leadingpT_l, "leadingpT_l/D");
    outputTree->Branch("l_e_phi", &l_e_phi, "l_e_phi/D");
    outputTree->Branch("l_ep_phi", &l_ep_phi, "l_ep_phi/D");
    outputTree->Branch("l_mu_phi", &l_mu_phi, "l_mu_phi/D");
    outputTree->Branch("l_mup_phi", &l_mup_phi, "l_mup_phi/D");

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
        
        //if(Mass > 140.){
            //count = count + 1;
            for (int j = 0; j < 10; j++){
                //calculate inviriant mass
                if(pid[j] == 11 || pid[j] == -11 || pid[j] == 13 || pid[j] == -13){
                    have_l = have_l + 1;//count lepton number

                    px_l = px_l + px[j];
                    py_l = py_l + py[j];
                    pz_l = pz_l + pz[j];
                    E_l = E_l + E[j];
                    
                    if(pid[j] == 11) l_e_phi = phi[j];
                    else if(pid[j] == -11) l_ep_phi = phi[j];
                    else if(pid[j] == 13) l_mu_phi = phi[j];
                    else if(pid[j] == -13) l_mup_phi = phi[j];
                
                    leading_pT_l = pT[j];
                    leading_l_No = j;
                    if (leading_pT_tem_l >= pT[j]){
                        leading_pT_l = leading_pT_tem_l;//calculate leading pT
                        leading_l_No = leading_l_No_tem;
                    }
                    leading_pT_tem_l = leading_pT_l;
                    leading_l_No_tem = leading_l_No;

            }

                if(pid[j] == 230 || pid[j] == 231 || pid[j] == 232 || pid[j] == 23) {

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

                        if(pid[je] == -11 && moth1[j] == moth1[je] && (pid[moth1[j]] == 230 ||pid[moth1[j]] == 231 ||pid[moth1[j]] ==232 || pid[moth1[j]] ==23)){//select electron pairs from z(maybe on-shell)
                            px_ee = px[j] + px[je];
                            py_ee = py[j] + py[je];
                            pz_ee = pz[j] + pz[je];
                            E_ee = E[j] + E[je];
                            mom_ee.SetPxPyPzE(px_ee, py_ee, pz_ee, E_ee);
                            eeinv=mom_ee.M();//ee pair invmass
                    }
                }
            }
                if(pid[j] == 13){

                    for(int jm = 0; jm < 10 ; jm++){//find muon pairs

                        if(pid[jm] == -13 && moth1[j] == moth1[jm] && (pid[moth1[j]] == 230 ||pid[moth1[j]] == 231 ||pid[moth1[j]] ==232||pid[moth1[j]] ==23)){//select muon pairs from z(maybe on-shell)
                            px_mm = px[j] + px[jm];
                            py_mm = py[j] + py[jm];
                            pz_mm = pz[j] + pz[jm];
                            E_mm = E[j] + E[jm];
                            mom_mm.SetPxPyPzE(px_mm, py_mm, pz_mm, E_mm);
                            mminv=mom_mm.M();//mumu pair invmass
                            //cout << mom_mm.M() << " ";
                    }
                }
            }

        }

        //}
        
                
        mom.SetPxPyPzE(px_l, py_l, pz_l, E_l);//fill 4l Lorentz vec
        //cout << have_z << " ";
        //Fill Histgram                   
        if(have_z != 0){//choose 2 z event 
            leadingpT_z = leading_pT;
            leading_z_eta = eta[leading_z_No];
            //cout << leadingpT_z << " "<< leading_z_eta << endl;
        }
        //else{leadingpT_z =0, leading_z_eta =0;}
        if(have_l == 4){//final states must contain 4l
            leadingpT_l = leading_pT_l;
            leading_l_eta = eta[leading_l_No];
            //l_phi->Fill(tot_phi);
            inv_mass = mom.M(); 
        } 

        outputTree->Fill();
        
        //set all array elements 0 to avoid mixing with next event
        memset(pz, 0, sizeof(pz)), memset(px, 0, sizeof(px)), memset(py, 0, sizeof(py));
        memset(E, 0, sizeof(E)), memset(pT, 0, sizeof(pT));
        memset(pid, 0, sizeof(pid)),memset(eta, 0, sizeof(eta)), memset(phi, 0, sizeof(phi));
        memset(moth1, 0, sizeof(moth1)),memset(moth2, 0, sizeof(moth2));

    }

    outputTree->Write();

    file->Close();
    ana->Close();

    cout << count << endl;

}
}