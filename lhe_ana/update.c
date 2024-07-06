#include "stdio.h"

void update(){

    TFile *filename = new TFile("/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/mg5condor/gg4l_tot/gg4m/jobs/rootfile/total.root", "UPDATE");

    TTree *tree = (TTree*)filename->Get("LHEF");

    int pid[10], n;
    double px[10], py[10], pz[10], E[10];
    double pT[10];//, eta[4], phi[4];
    int moth1[10],moth2[10];
    TLorentzVector mom, mom_ee;

    tree->SetBranchAddress("Particle.Px", &px);
    tree->SetBranchAddress("Particle.Py", &py);
    tree->SetBranchAddress("Particle.Pz", &pz);
    tree->SetBranchAddress("Particle.E", &E);
    tree->SetBranchAddress("Particle.PID", &pid);
    tree->SetBranchAddress("Particle.PT", &pT);
    tree->SetBranchAddress("Particle.Mother1", &moth1);
    tree->SetBranchAddress("Particle.Mother2", &moth2);

    n = tree->GetEntries();
    cout << n << endl;

    float inv_mass;
    TBranch *b_inv_mass = tree->Branch("inv_mass",&inv_mass,"inv_mass/F");

    for (int i = 0; i < n; i++){
        tree->GetEntry(i);
        double px_l=0, py_l=0, pz_l=0, E_l=0, eta_l=0, phi_l=0, pT_l=0;
        double px_ee=0, py_ee=0, pz_ee=0, pt_ee=0, E_ee=0;
        double delta_eta=0, delta_eta_tem=0;
        double delta_phi=0, delta_phi_tem=0;
        double leading_pT=0, leading_pT_tem=0;
        bool have_Z = false;
        
        for (int j = 0; j < 10; j++){//calculate inviriant mass
            if(pid[j] == 11 || pid[j] == -11 || pid[j] == 13 || pid [j] == -13){
                px_l = px_l + px[j];
                py_l = py_l + py[j];
                pz_l = pz_l + pz[j];
                E_l = E_l +E[j];
            }

        }
        //set all array elements 0 to avoid mixing with next event
        memset(pz, 0, sizeof(pz)), memset(px, 0, sizeof(px)), memset(py, 0, sizeof(py));
        memset(E, 0, sizeof(E)), memset(pT, 0, sizeof(pT));
        memset(pid, 0, sizeof(pid));
        memset(moth1, 0, sizeof(moth1));
        memset(moth2, 0, sizeof(moth2));
        
        mom.SetPxPyPzE(px_l, py_l, pz_l, E_l);//calculate inv mass
        inv_mass = mom.M();

        b_inv_mass->Fill();
    }
    tree->Write("", TObject::kOverwrite);
    filename->Close();
}
