//////////////////////////////////////////////Draw some hists
void Draw(TH1F *h_tot, TH1F *h_bkg, TH1F *h_sig, int gap, int l_edge, int r_edge, char *xname, char *yname){
    
    TCanvas *c1 = new TCanvas;

    //c1->SetLogy();
    h_bkg->GetXaxis()->SetTitle(xname);
    h_bkg->GetYaxis()->SetTitle(yname);
    h_bkg->SetStats(0);
    h_bkg->Scale(1.54/h_bkg->Integral());
    h_bkg->SetLineColor(kRed);
    //h_bkg->SetMaximum(0.2);
    //h_bkg->SetMinimum(0);
    h_bkg->Draw("hist");
    
    h_tot->Scale(1.475/h_tot->Integral());
    h_tot->Draw("hist same");

    TH1F *h_s_inter = new TH1F("h_s_inter", " ", gap, l_edge, r_edge);

    h_s_inter->Add(h_tot, h_bkg, -1, 1);
    h_s_inter->SetLineColor(kBlack);
    h_s_inter->Scale(0.065/h_s_inter->Integral());
    h_s_inter->Draw("hist same");

    TLegend *legend0 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend0->AddEntry(h_tot, "tot", "l");
    legend0->AddEntry(h_bkg, "bkg", "l");
    legend0->AddEntry(h_s_inter, "-(S+I)", "l");
    legend0->Draw();
    c1->SaveAs("./c1.png");
    
    TCanvas *c2 = new TCanvas;

    h_sig->GetXaxis()->SetTitle(xname);
    h_sig->GetYaxis()->SetTitle(yname);
    h_sig->SetStats(0);
    h_sig->Scale(0.05974/h_sig->Integral());
    h_sig->Draw("h");
    c2->SaveAs("./c2.png");

    TCanvas *c3 = new TCanvas;

    TH1F *h_inter_s = new TH1F("h_inter_s", " ", gap, l_edge, r_edge);
    h_inter_s->Add(h_tot, h_bkg, 1, -1);

    h_inter_s->GetXaxis()->SetTitle(xname);
    h_inter_s->GetYaxis()->SetTitle(yname);
    h_inter_s->SetStats(0);
    h_inter_s->SetLineColor(kBlue);
    h_inter_s->SetMaximum(0.015);
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
    c3->SaveAs("./c3.png");

    TCanvas *c4 = new TCanvas;

    c4->SetLogy();
    //c4->SetLogx();

    h_bkg->GetXaxis()->SetTitle(xname);
    h_bkg->GetYaxis()->SetTitle(yname);
    h_bkg->SetStats(0);
    h_bkg->Scale(1.54/h_bkg->Integral());
    h_bkg->SetLineColor(kRed);
    //h_bkg->SetMaximum(1e4);
    //h_bkg->SetMinimum(1e-7);
    h_bkg->Draw("hist");

    h_tot->Scale(1.475/h_tot->Integral());
    h_tot->SetLineColor(kBlue);
    h_tot->Draw("hist same");

    h_sig->Scale(0.05974/h_sig->Integral());
    h_sig->SetLineColor(kBlack);
    h_sig->Draw("hist same");

    TLegend *legend2 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend2->AddEntry(h_tot, "tot", "l");
    legend2->AddEntry(h_sig, "S", "l");
    legend2->AddEntry(h_bkg, "gg bkg", "l");
    legend2->Draw();
    c4->SaveAs("./c4.png");

    // char pic[] = "./c4_";
    // char class[] = ".png";

    // std::string &whole = std::string(pic) + std::string(xname) +std::string(class);

    // char c[] = whole.c_str();

}


void Draw_Norm(TH1F *h_tot, TH1F *h_bkg, TH1F *h_sig, int gap, int l_edge, int r_edge, char *xname, char *yname){

    TCanvas *c = new TCanvas();

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

    c->SaveAs("./c.png");

}
