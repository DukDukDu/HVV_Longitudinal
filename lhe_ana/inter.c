///////////////////////////////////////////////////////////////////////////////////////////////////////////
////        This file can read from LHE file and Draw some plots, and if you want                     /////
////        to add new kinematic variables or find different final particles, please                  ///// 
////        add them in read_lhe.h or read_lhe_4l.h. char xaxistitle and char yaxis                   /////
////        are the name of the hist you want to draw. You'd better keep hists' axis                  ///// 
////        limits and bin number same with the parameter you send to the function                    /////
////        Draw. If you want to plot normalized hist please choose Draw_Norm, and                    /////
////        if you want to scale hist to cross section, choose Draw.                                  /////
////        NOTICE When you use this file, you'd better have draw.h and read_lhe.h                    /////
///////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "stdio.h"
#include "draw.h"
#include "read_lhe_zz.h"
#include "read_lhe_4l.h"

using namespace LHE;
using namespace LHE_4l;
///////////////////////////////////////////main function
void inter(){

//////////////////////zz final state////////////////////////////////////

    TFile *f1 = new TFile("../ggzz/gg_tot.root", "READ");
    TFile *f2 = new TFile("../ggzz/gg_bkg.root", "READ");
    TFile *f3 = new TFile("../ggzz/gg_sig.root", "READ");

    TH1F *h_tot = new TH1F("h_tot", " ", 50, 0, 1000);
    TH1F *h_bkd = new TH1F("h_bkg", " ", 50, 0, 1000);
    TH1F *h_sig = new TH1F("h_sig", " ", 30, 0, 3000);

    TH1F *lpt_tot = new TH1F("lpt_tot", " ", 50, 0, 500);
    TH1F *lpt_bkd = new TH1F("lpt_bkg", " ", 50, 0, 500);
    TH1F *lpt_sig = new TH1F("lpt_sig", " ", 50, 0, 500);

    TH1F *deltaeta_tot = new TH1F("deltaeta_tot", " ", 50, 0, 10);
    TH1F *deltaeta_bkd = new TH1F("deltaeta_bkg", " ", 50, 0, 10);
    TH1F *deltaeta_sig = new TH1F("deltaeta_sig", " ", 50, 0, 10);

    TH1F *deltaphi_tot = new TH1F("deltaphi_tot", " ", 40, 0, 4);
    TH1F *deltaphi_bkd = new TH1F("deltaphi_bkg", " ", 40, 0, 4);
    TH1F *deltaphi_sig = new TH1F("deltaphi_sig", " ", 40, 0, 4);

///////////////////////4l final state////////////////////////////////////

    TFile *f3_4l = new TFile("/publicfs/cms/user/mingxuanzhang/gridpack/simulation_tool/mg5condor/gg4l_tot/gg2e2m/jobs/rootfile/total.root", "READ");
    
    TH1F *h_tot_4l = new TH1F("h_tot_4l", " ", 50, 0, 1000);
    TH1F *lpt_tot_4l = new TH1F("lpt_tot_4l", " ", 50, 0, 500);
    TH1F *ptz_tot_4l = new TH1F("ptz_tot_4l", " ", 500, 0, 500);
    TH1F *eeinv_tot_4l = new TH1F("eeinv_tot_4l", " ", 500, 0, 500);

//////////////////////////////////////////////////////////////////////////

    //LHE::Fill_histogram(f1, h_tot, lpt_tot, deltaeta_tot, deltaphi_tot);
    //LHE::Fill_histogram(f2, h_bkd, lpt_bkd, deltaeta_bkd, deltaphi_bkd);
    LHE_4l::Fill_histogram(f3_4l, h_tot_4l, ptz_tot_4l, eeinv_tot_4l);
    //LHE_4l::Fill_histogram(g4e_ch, invmass_ch, ch_ptz, eeinvch);

    //LHE_4l::Fill_histogram(f3_4l, h_sig_4l, lpt_sig_4l);


///////////////////////////////////////examine the fortran code ///////////
       
    // TFile *g4e_no = new TFile("../g4e/ppzz4e_no.root");
    // TFile *g4e_ch = new TFile("../g4e/ppzz4e.root");

    // TH1F *invmass_no = new TH1F("invmass_no", " ", 50, 0, 1000);
    // TH1F *invmass_ch = new TH1F("invmass_ch", " ", 50, 0, 1000);

    // TH1F *no_ptz = new TH1F("no_ptz", " ", 400, 40, 500);
    // TH1F *ch_ptz = new TH1F("ch_ptz", " ", 400, 40, 500);

    // TH1F *eeinvno = new TH1F("eeinvno", " ", 20, 0, 200);
    // TH1F *eeinvch = new TH1F("eeinvno", " ", 20, 0, 200);
//////////////////////////////////////////////////////////////////////////

    TCanvas *c = new TCanvas;
    h_tot_4l->GetXaxis()->SetTitle("Mass (GeV)");
    h_tot_4l->GetYaxis()->SetTitle("Density");
    h_tot_4l->SetLineColor(kBlue);
    //h_tot_4l->SetStats(0);
    h_tot_4l->Draw("hist");

    c->SaveAs("./pic/invmass.png");
    
    TCanvas *c1 = new TCanvas;
    ptz_tot_4l->GetXaxis()->SetTitle(" ee pTco (GeV)");
    ptz_tot_4l->GetYaxis()->SetTitle("Events");
    ptz_tot_4l->Draw("hist");
    c1->SaveAs("./pic/lptz.png");

    TCanvas *c2 = new TCanvas;
    eeinv_tot_4l->GetXaxis()->SetTitle(" ee inv_mass (GeV)");
    eeinv_tot_4l->GetYaxis()->SetTitle("Events");
    eeinv_tot_4l->Draw("hist");
    c2->SaveAs("./pic/eeinv.png");

    cout << eeinv_tot_4l->Integral() << endl;
    //Draw_Norm(lpt_tot, lpt_bkd, lpt_sig, 50, 0, 500, xaxistitle, yaxis);
    //Draw_Norm(deltaeta_tot, deltaeta_bkd, deltaeta_sig, 50, 0, 10, xaxistitle, yaxis);
    //Draw_Norm(deltaphi_tot, deltaphi_bkd, deltaphi_sig, 40, 0, 4, xaxistitle,yaxis);
    //Draw_Norm(h_tot, h_bkd, h_sig, 50, 0, 1000, xaxistitle, yaxis);
}