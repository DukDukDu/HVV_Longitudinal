//////////////////////////////////////////////Draw some hists
void Draw(TH1F *h_tot, TH1F *h_bkg, TH1F *h_sig, int gap, int l_edge, int r_edge,\
          char *xname, char *yname, double sx_tot, double sx_bkg, double sx_sig,\
          string name){
    
    string pathpng = "./pic/gg4m/";
    string png1 = "_1.png", png2 = "_2.png", png3 = "_3.png", png4 = "_4.png";
    string res1 = pathpng+name+png1, res2 = pathpng+name+png2, res3 = pathpng+name+png3, res4 = pathpng+name+png4;
    const char *c_res1 = res1.c_str();
    const char *c_res2 = res2.c_str();
    const char *c_res3 = res3.c_str();
    const char *c_res4 = res4.c_str();

    TCanvas *c1 = new TCanvas;

    //c1->SetLogy();
    h_bkg->GetXaxis()->SetTitle(xname);
    h_bkg->GetYaxis()->SetTitle(yname);
    h_bkg->SetStats(0);
    h_bkg->Scale(sx_bkg/h_bkg->Integral());
    h_bkg->SetLineColor(kRed);
    //h_bkg->SetMaximum(0.);
    //h_bkg->SetMinimum(0);
    h_bkg->Draw("hist");
    
    h_tot->Scale(sx_tot/h_tot->Integral());
    h_tot->Draw("hist same");

    TH1F *h_s_inter = new TH1F("h_s_inter", " ", gap, l_edge, r_edge);

    h_s_inter->Add(h_tot, h_bkg, -1, 1);
    h_s_inter->SetLineColor(kBlack);
    h_s_inter->Scale((sx_bkg-sx_tot)/h_s_inter->Integral());
    h_s_inter->Draw("hist same");

    TLegend *legend0 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend0->AddEntry(h_tot, "tot", "l");
    legend0->AddEntry(h_bkg, "bkg", "l");
    legend0->AddEntry(h_s_inter, "-(S+I)", "l");
    legend0->Draw();
    c1->SaveAs(c_res1);
    
    TCanvas *c2 = new TCanvas;

    h_sig->GetXaxis()->SetTitle(xname);
    h_sig->GetYaxis()->SetTitle(yname);
    h_sig->SetStats(0);
    h_sig->Scale(sx_sig/h_sig->Integral());
    h_sig->Draw("h");
    c2->SaveAs(c_res2);

    TCanvas *c3 = new TCanvas;

    TH1F *h_inter_s = new TH1F("h_inter_s", " ", gap, l_edge, r_edge);
    h_inter_s->Add(h_tot, h_bkg, 1, -1);

    h_inter_s->GetXaxis()->SetTitle(xname);
    h_inter_s->GetYaxis()->SetTitle(yname);
    h_inter_s->SetStats(0);
    h_inter_s->SetLineColor(kBlue);
    h_inter_s->SetMaximum(0.1);
    h_inter_s->SetMinimum(-0.02);
    h_inter_s->Draw("h");
   
    h_sig->SetLineColor(kBlack);
    h_sig->Draw("h same");

    h_bkg->SetLineColor(kRed);
    h_bkg->Draw("h same");

    TLegend *legend1 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend1->AddEntry(h_inter_s, "S + I", "l");
    legend1->AddEntry(h_sig, "S", "l");
    legend1->AddEntry(h_bkg, "gg bkg", "l");
    legend1->Draw();
    c3->SaveAs(c_res3);

    TCanvas *c4 = new TCanvas;

    c4->SetLogy();
    //c4->SetLogx();

    h_bkg->GetXaxis()->SetTitle(xname);
    h_bkg->GetYaxis()->SetTitle(yname);
    h_bkg->SetStats(0);
    h_bkg->Scale(sx_bkg/h_bkg->Integral());
    h_bkg->SetLineColor(kRed);
    //h_bkg->SetMaximum(1e4);
    //h_bkg->SetMinimum(1e-7);
    h_bkg->Draw("hist");

    h_tot->Scale(sx_tot/h_tot->Integral());
    h_tot->SetLineColor(kBlue);
    h_tot->Draw("hist same");

    h_sig->Scale(sx_sig/h_sig->Integral());
    h_sig->SetLineColor(kBlack);
    h_sig->Draw("hist same");

    TLegend *legend2 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend2->AddEntry(h_tot, "tot", "l");
    legend2->AddEntry(h_sig, "S", "l");
    legend2->AddEntry(h_bkg, "gg bkg", "l");
    legend2->Draw();
    c4->SaveAs(c_res4);

}


void Draw_Norm(TH1F *h_tot, TH1F *h_bkg, TH1F *h_sig, int gap, int l_edge,\
               int r_edge, char *xname, char *yname, string name){

    TCanvas *c_norm = new TCanvas();

    string pathpng = "./pic/gg4m/";
    string png = ".png";

    string result = pathpng + name + png;
    const char *c_res = result.c_str();

    h_bkg->GetXaxis()->SetTitle(xname);
    h_bkg->GetYaxis()->SetTitle(yname);
    h_bkg->SetStats(0);
    h_bkg->Scale(1/h_bkg->Integral());
    h_bkg->SetLineColor(kRed);
    //h_bkg->SetMaximum(0.15);
    //h_bkg->SetMinimum(0);
    h_bkg->Draw("hist");

    h_tot->Scale(1/h_tot->Integral());
    h_tot->SetLineColor(kBlue);
    h_tot->Draw("hist same");

    h_sig->Scale(1/h_sig->Integral());
    h_sig->SetLineColor(kBlack);
    h_sig->Draw("hist same");

    TLegend *legend3 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend3->AddEntry(h_tot, "tot", "l");
    legend3->AddEntry(h_sig, "S", "l");
    legend3->AddEntry(h_bkg, "gg bkg", "l");
    legend3->Draw();

    c_norm->SaveAs(c_res);

}
