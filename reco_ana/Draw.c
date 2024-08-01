void draw_fun(TTree *tree_tot, TTree *tree_bkg, TTree *tree_sig, double nbin, double l_x, double r_x, string name, string x_name){

    TCanvas *c1 = new TCanvas;

    string pathpng = "./pic/gg2e2m/";
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
    
    TCanvas *c1 = new TCanvas;
    
    string pathpng = "./pic/gg2e2m/";
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

    h1->Scale(gg2e2m_tot_xs/h1->Integral());
    h1->SetStats(0);
    h1->GetXaxis()->SetTitle(name_x);
    h1->GetYaxis()->SetTitle("Density");
    h1->SetLineColor(kBlack);
    h1->SetMaximum(0.015);
    h1->SetMinimum(-0.02);
    h1->Draw("hist");
    h2->Scale(gg2e2m_bkg_xs/h2->Integral());
    h2->SetLineColor(kRed);
    h2->Draw("hist same");
    h3->Scale(gg2e2m_sig_xs/h3->Integral());
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


    c1->SaveAs(c_res);
}

void Draw(){
    TFile *f_tot = new TFile("gg2e2m_tot.root", "READ");
    TFile *f_bkg = new TFile("gg2e2m_bkg.root", "READ");
    TFile *f_sig = new TFile("gg2e2m_sig.root", "READ");

    TTree *tree_tot = (TTree*)f_tot->Get("Events");
    TTree *tree_bkg = (TTree*)f_bkg->Get("Events");
    TTree *tree_sig = (TTree*)f_sig->Get("Events");

    double gg2e2m_tot_xs = 1.66;
    double gg2e2m_bkg_xs = 1.74;
    double gg2e2m_sig_xs = 0.09585;
    
    string inv_mass = "inv_mass";
    string x_inv_mass = "inv mass(GeV)";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 1000, inv_mass, x_inv_mass);

    string ee_inv_mass = "ee_inv_mass";
    string x_ee_inv_mass = "ee inv mass(GeV)";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 110, 40, 130, ee_inv_mass, x_ee_inv_mass);

    string mm_inv_mass = "mm_inv_mass";
    string x_mm_inv_mass = "#mu#mu inv mass(GeV)";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 110, 40, 130, mm_inv_mass, x_mm_inv_mass);

    string ee_pt = "ee_pt";
    string x_ee_pt = "ee p_{T}(GeV)";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 500, ee_pt, x_ee_pt);

    string mm_pt = "mm_pt";
    string x_mm_pt = "#mu#mu p_{T}(GeV)";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 100, 0, 500, mm_pt, x_mm_pt);

    string delta_eta_e = "delta_eta_e";
    string x_delta_eta_e = "#Delta #eta_{ee}";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_eta_e, x_delta_eta_e);

    string delta_eta_m = "delta_eta_m";
    string x_delta_eta_m = "#Delta #eta_{#mu#mu}";
    draw_fun_xs(tree_tot, tree_bkg, tree_sig, 50, 0, 4, delta_eta_m, x_delta_eta_m);
}