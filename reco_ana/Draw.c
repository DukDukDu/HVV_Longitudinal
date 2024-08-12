void draw_fun(TTree *tree_tot, TTree *tree_bkg, TTree *tree_sig, double nbin, double l_x, double r_x, string name, string x_name){

    TCanvas *c1 = new TCanvas;

    //c1->SetLogx();
    c1->SetLogy();

    string pathpng = "./pic/gg4m/";
    string png = ".png";
    string result = pathpng + name + png;
    const char *c_res = result.c_str();

    string s_h1 = ">>h1";
    string s_h2 = ">>h2";
    string s_h3 = ">>h3";

    string res_h1 = name + s_h1;
    string res_h2 = name + s_h2;
    string res_h3 = name + s_h3;

    const char *h1_res = res_h1.c_str();
    const char *h2_res = res_h2.c_str();
    const char *h3_res = res_h3.c_str();

    const char *name_x = x_name.c_str();

    TH1F *h1 = new TH1F("h1", " ", nbin, l_x, r_x);
    TH1F *h2 = new TH1F("h2", " ", nbin, l_x, r_x);
    TH1F *h3 = new TH1F("h3", " ", nbin, l_x, r_x);

    tree_tot->Draw(h1_res);
    tree_bkg->Draw(h2_res);
    tree_sig->Draw(h3_res);

    h1->Scale(1/h1->Integral());
    h1->SetStats(0);
    h1->GetXaxis()->SetTitle(name_x);
    h1->GetYaxis()->SetTitle("Density");
    h1->SetLineColor(kBlack);
    h1->SetMaximum(0.8);
    h1->Draw("hist");
    h2->Scale(1/h2->Integral());
    h2->SetLineColor(kRed);
    h2->Draw("hist same");
    h3->Scale(1/h3->Integral());
    h3->SetLineColor(kBlue);
    h3->Draw("hist same");

    TLegend *legend0 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend0->AddEntry(h1, "tot", "l");
    legend0->AddEntry(h2, "bkg", "l");
    legend0->AddEntry(h3, "sig", "l");
    legend0->Draw();

    c1->SaveAs(c_res);
}

void draw_fun_xs(TTree *tree_tot, TTree *tree_bkg, TTree *tree_sig, double nbin, double l_x, double r_x, string name, string x_name){

    double gg2e2m_tot_xs = 1.66;
    double gg2e2m_bkg_xs = 1.74;
    double gg2e2m_sig_xs = 0.09585;
    double gg4e_tot_xs = 0.8231;
    double gg4e_bkg_xs = 0.8656;
    double gg4e_sig_xs = 0.04811;
    double gg4m_tot_xs = 0.8231;
    double gg4m_bkg_xs = 0.8656;
    double gg4m_sig_xs = 0.04811;

    TCanvas *c1 = new TCanvas;
    //c1->SetLogy();
    
    string pathpng = "./pic/gg4m/";
    string png = "xs.png";
    string result = pathpng + name + png;
    const char *c_res = result.c_str();

    string s_h1 = ">>h1";
    string s_h2 = ">>h2";
    string s_h3 = ">>h3";

    string res_h1 = name + s_h1;
    string res_h2 = name + s_h2;
    string res_h3 = name + s_h3;

    const char *h1_res = res_h1.c_str();
    const char *h2_res = res_h2.c_str();
    const char *h3_res = res_h3.c_str();

    const char *name_x = x_name.c_str();

    TH1F *h1 = new TH1F("h1", " ", nbin, l_x, r_x);
    TH1F *h2 = new TH1F("h2", " ", nbin, l_x, r_x);
    TH1F *h3 = new TH1F("h3", " ", nbin, l_x, r_x);

    tree_tot->Draw(h1_res);
    tree_bkg->Draw(h2_res);
    tree_sig->Draw(h3_res);

    TH1F *h_inter_s = new TH1F("h_inter_s", " ", nbin, l_x, r_x);

    h1->Scale(gg4e_tot_xs/h1->Integral());
    h1->SetStats(0);
    h1->GetXaxis()->SetTitle(name_x);
    h1->GetYaxis()->SetTitle("Density");
    h1->SetLineColor(kBlack);
    h1->SetMaximum(0.03);
    h1->SetMinimum(-0.01);
    h1->Draw("hist");
    h2->Scale(gg4e_bkg_xs/h2->Integral());
    h2->SetLineColor(kRed);
    h2->Draw("hist same");
    h3->Scale(gg4e_sig_xs/h3->Integral());
    h3->SetLineColor(kBlue);
    h3->Draw("hist same");
    h_inter_s->Add(h1, h2, 1, -1);
    h_inter_s->SetLineColor(kGreen);
    h_inter_s->Draw("hist same");

    TLegend *legend0 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend0->AddEntry(h1, "tot", "l");
    legend0->AddEntry(h2, "bkg", "l");
    legend0->AddEntry(h3, "sig", "l");
    legend0->AddEntry(h_inter_s, "s+inter", "l");
    legend0->Draw();

    // for(int i1 = 1; i1 < nbin+1; i1++){
    //     cout << h1->GetBinContent(i1)*1e6 << ", " << endl;
    // }
    // cout << "----------------------" << endl;
    // for(int i2 = 1; i2 < nbin+1; i2++){
    //     cout << h2->GetBinContent(i2)*1e6 << ", " << endl;
    // }
    // cout << "----------------------" << endl;
    // for(int i3 = 1; i3 < nbin+1; i3++){
    //     cout << h3->GetBinContent(i3)*1e6 << ", " << endl;
    // }

    // cout << "----------------------" << endl;
    // for(int i4 = 1; i4 < nbin+1; i4++){
    //     cout << h_inter_s->GetBinContent(i4)*1e6 << ", " << endl;
    // }
    c1->SaveAs(c_res);
}

void Draw(){
    TFile *f_tot = new TFile("gg4m_tot.root", "READ");
    TFile *f_bkg = new TFile("gg4m_bkg.root", "READ");
    TFile *f_sig = new TFile("gg4m_sig.root", "READ");

    TTree *tree_tot = (TTree*)f_tot->Get("Events");
    TTree *tree_bkg = (TTree*)f_bkg->Get("Events");
    TTree *tree_sig = (TTree*)f_sig->Get("Events");
    
    string inv_mass = "inv_mass";
    string x_inv_mass = "inv mass(GeV)";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 1000, inv_mass, x_inv_mass);

    // string prob = "D_value";
    // string x_prob = "D_value";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 40, 0, 0.7, prob, x_prob);
    //draw_fun(tree_tot, tree_bkg, tree_sig, 50, 0.8, 1, prob, x_prob);

    // string mumu1_inv_mass = "mumu1_inv_mass";
    // string x_mumu1_inv_mass = "leading p_{T} p_{#mu#mu} inv mass(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 110, 40, 130, mumu1_inv_mass, x_mumu1_inv_mass);

    // string mumu2_inv_mass = "mumu2_inv_mass";
    // string x_mumu2_inv_mass = "subleading p_{T} p_{#mu#mu} inv mass(GeV)";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 110, 40, 130, mumu2_inv_mass, x_mumu2_inv_mass);

    // string delta_mumu1_eta = "delta_mumu1_eta";
    // string x_delta_mumu1_eta = "leading p_{T} #Delta #eta_{#mu#mu}";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_mumu1_eta, x_delta_mumu1_eta);

    // string delta_mumu2_eta = "delta_mumu2_eta";
    // string x_delta_mumu2_eta = "subleading p_{T} #Delta #eta_{#mu#mu}";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_mumu2_eta, x_delta_mumu2_eta);

    string delta_mumu1_phi = "delta_mumu1_phi";
    string x_delta_mumu1_phi = "leading p_{T} #Delta #phi_{#mu#mu}";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_mumu1_phi, x_delta_mumu1_phi);

    // string delta_mumu2_phi = "delta_mumu2_phi";
    // string x_delta_mumu2_phi = "subleading p_{T} #Delta #phi_{#mu#mu}";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_mumu2_phi, x_delta_mumu2_phi);

    // string mumu1_pt = "mumu1_pt";
    // string x_mumu1_pt = "leading #mu#mu p_{T}(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 500, mumu1_pt, x_mumu1_pt);

    // string mumu2_pt = "mumu2_pt";
    // string x_mumu2_pt = "subleading #mu#mu p_{T}(GeV)";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 100, 0, 500, mumu2_pt, x_mumu2_pt);

    // string ee1_inv_mass = "ee1_inv_mass";
    // string x_ee1_inv_mass = "leading p_{T} p_{ee} inv mass(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 110, 40, 130, ee1_inv_mass, x_ee1_inv_mass);

    // string ee2_inv_mass = "ee2_inv_mass";
    // string x_ee2_inv_mass = "subleading p_{T} p_{ee} inv mass(GeV)";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 110, 40, 130, ee2_inv_mass, x_ee2_inv_mass);

    // string delta_ee1_eta = "delta_ee1_eta";
    // string x_delta_ee1_eta = "leading p_{T} #Delta #eta_{ee}";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_ee1_eta, x_delta_ee1_eta);

    // string delta_ee2_eta = "delta_ee2_eta";
    // string x_delta_ee2_eta = "#subleading p_{T} Delta #eta_{ee2}";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_ee2_eta, x_delta_ee2_eta);

    // string delta_ee1_phi = "delta_ee1_phi";
    // string x_delta_ee1_phi = "leading p_{T} #Delta #phi_{ee}";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 60, 0, 6, delta_ee1_phi, x_delta_ee1_phi);

    // string delta_ee2_phi = "delta_ee2_phi";
    // string x_delta_ee2_phi = "subleading p_{T} #Delta #phi_{ee}";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 60, 0, 6, delta_ee2_phi, x_delta_ee2_phi);

    // string ee1_pt = "ee1_pt";
    // string x_ee1_pt = "leading ee p_{T}(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 500, ee1_pt, x_ee1_pt);

    // string ee2_pt = "ee2_pt";
    // string x_ee2_pt = "leading ee p_{T}(GeV)";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 100, 0, 500, ee2_pt, x_ee2_pt);

    // string ee_inv_mass = "ee_inv_mass";
    // string x_ee_inv_mass = "ee inv mass(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 110, 40, 130, ee_inv_mass, x_ee_inv_mass);

    // string mm_inv_mass = "mm_inv_mass";
    // string x_mm_inv_mass = "#mu#mu inv mass(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 110, 40, 130, mm_inv_mass, x_mm_inv_mass);

    // string ee_pt = "ee_pt";
    // string x_ee_pt = "ee p_{T}(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 500, ee_pt, x_ee_pt);

    // string mm_pt = "mm_pt";
    // string x_mm_pt = "#mu#mu p_{T}(GeV)";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 500, mm_pt, x_mm_pt);

    // string delta_eta_e = "delta_eta_e";
    // string x_delta_eta_e = "#Delta #eta_{ee}";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_eta_e, x_delta_eta_e);

    // string delta_eta_m = "delta_eta_m";
    // string x_delta_eta_m = "#Delta #eta_{#mu#mu}";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_eta_m, x_delta_eta_m);

    // string delta_phi_m = "delta_phi_m";
    // string x_delta_phi_m = "#Delta #phi_{#mu#mu}";
    // draw_fun(tree_tot, tree_bkg, tree_sig, 60, 0, 6, delta_phi_m, x_delta_phi_m);

    // string delta_phi_e = "delta_phi_e";
    // string x_delta_phi_e = "#Delta #phi_{ee}";
    // draw_fun_xs(tree_tot, tree_bkg, tree_sig, 60, 0, 6, delta_phi_e, x_delta_phi_e);
}