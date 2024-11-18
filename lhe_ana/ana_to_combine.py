import ROOT as R 
import numpy as np
import sys

bkg = R.TFile("./2e2m_bkg.root", "READ")
total_125 = R.TFile("./mh125_total.root", "READ")

tot = R.TFile("./mh125_total.root", "READ")
sig = R.TFile("./mh125_sig.root", "READ")
# bkg_ll = R.TFile("./2e2m_bkg_ll.root", "READ")
# bkg_tt = R.TFile("./2e2m_bkg_tt.root", "READ")
# sig = R.TFile("./2e2m_sig.root", "READ")
# sig_ll = R.TFile("./2e2m_sig_ll.root", "READ")
# sig_tt = R.TFile("./2e2m_sig_tt.root", "READ")
# total = R.TFile("./2e2m_total.root", "READ")
# tot_ll = R.TFile("./2e2m_tot_ll.root", "READ")
# tot_tt = R.TFile("./2e2m_tot_tt.root", "READ")
# qqzz = R.TFile("./2e2m_qqzz.root", "READ")

out = R.TFile("./forCombine_mh125.root", "RECREATE")
folder = out.mkdir("eemm")
folder.cd()

# nb_bkg, nb_bkg_ll, nb_bkg_tt = 0.3397*3000, 0.03177*3000, 0.2925*3000
# nb_sig, nb_sig_ll, nb_sig_tt = 0.07562*3000, 0.07401*3000, 0.001472*3000
# nb_total, nb_tot_ll, nb_tot_tt = 0.31*3000, 0.01607*3000, 0.2808*3000

bkg_tree = bkg.Get("Events")
tot_tree = tot.Get("Events")
sig_tree = sig.Get("Events")
tot_tree_125 = total_125.Get("Events")
# bkg_ll_tree = bkg_ll.Get("Events")
# bkg_tt_tree = bkg_tt.Get("Events")
# sig_tree = sig.Get("Events")
# sig_ll_tree = sig_ll.Get("Events")
# sig_tt_tree = sig_tt.Get("Events")
# total_tree = total.Get("Events")
# tot_ll_tree = tot_ll.Get("Events")
# tot_tt_tree = tot_tt.Get("Events")
# qqzz_tree = qqzz.Get("Events")

bins = np.array([400, 400+75, 400+75*2, 400+75*3, 400+75*4, 400+75*4+100, 400+75*4+200, 400+75*4+300],dtype = 'double')

tot_160_evt = 3000*1.522
sig_160_evt = 3000*0.1228
tot_150_evt = 3000*1.525
sig_150_evt = 3000*0.11
tot_140_evt = 3000*1.519
sig_140_evt = 3000*0.1023
tot_130_evt = 3000*1.521
sig_130_evt = 3000*0.09803
tot_125_evt = 3000*1.511
sig_125_evt = 3000*0.09422
tot_100_evt = 3000*1.529
sig_100_evt = 3000*0.08527
tot_80_evt = 3000*1.53
sig_80_evt = 3000*0.08113
tot_50_evt = 3000*1.529
sig_50_evt = 3000*0.07751
bkg_evt = 3000*1.581

im_bkg = R.TH1F("im_bkg", " ", 20, 0, 1)
im_tot = R.TH1F("im_tot", " ", 20, 0, 1)
im_tot_125 = R.TH1F("im_tot_125", " ", 20, 0, 1)
im_sig = R.TH1F("im_sig", " ", 20, 0, 1)
data_obs = R.TH1F("data_obs", " ", 20, 0, 1)
im_inter = R.TH1F("im_inter", " ", 20, 0, 1)
im_all_bkgs = R.TH1F("im_all_bkgs", " ", 20, 0, 1)
# im_bkg_ll = R.TH1F("im_bkg_ll", " ", 20, 0, 1)
# im_bkg_tt = R.TH1F("im_bkg_tt", " ", 20, 0, 1)
# im_sig = R.TH1F("im_sig", " ", 20, 0, 1)
# im_sig_ll = R.TH1F("im_sig_ll", " ", 20, 0, 1)
# im_sig_tt = R.TH1F("im_sig_tt", " ", 20, 0, 1)
# im_total = R.TH1F("im_total", " ", 20, 0, 1)
# #im_total = R.TH1F("im_total", "total ", len(bins)-1 , bins)
# im_tot_ll = R.TH1F("im_tot_ll", " ", 20, 0, 1)
# im_tot_tt = R.TH1F("im_tot_tt", " ", 20, 0, 1)
# im_inter_ll = R.TH1F("im_inter_ll", " ", 20, 0, 1)
# im_inter_tt = R.TH1F("im_inter_tt", " ", 20, 0, 1)
# im_all_bkgs = R.TH1F("im_all_bkgs", " ", 20, 0, 1)
# im_qqzz = R.TH1F("im_qqzz", " ", 20, 0, 1)
# #im_qqzz = R.TH1F("im_qqzz", "qqzz ", len(bins)-1, bins)
# data_obs = R.TH1F("data_obs", " ", 20, 0, 1)
# forinter_tt = R.TH1F("forinter_tt", " ", 20, 0, 1)
# forsig = R.TH1F("forsig", " ", 20, 0, 1)

im_bkg.Sumw2()
im_inter.Sumw2()
im_sig.Sumw2()
data_obs.Sumw2()
# im_bkg_ll.Sumw2()
# im_bkg_tt.Sumw2()
# im_sig.Sumw2()
# im_sig_ll.Sumw2()
# im_sig_tt.Sumw2()
# im_total.Sumw2()
# im_tot_ll.Sumw2()
# im_tot_tt.Sumw2()
# im_inter_ll.Sumw2()
# im_inter_tt.Sumw2()
# im_qqzz.Sumw2()
# data_obs.Sumw2()
# forinter_tt.Sumw2()

bkg_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_bkg")
tot_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_tot")
tot_tree_125.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_tot_125")
sig_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_sig")

im_tot.Scale(tot_125_evt/im_tot.Integral())
im_sig.Scale(sig_125_evt/im_sig.Integral())


im_bkg.Scale(bkg_evt/im_bkg.Integral())
im_tot_125.Scale(tot_125_evt/im_tot_125.Integral())

data_obs.Add(im_tot_125, 1)
im_inter.Add(im_bkg, im_tot, 1, -1)

#im_sig.Write()
im_bkg.Write()
im_tot.Write()
data_obs.Write()

out.Close()



# bkg_ll_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_bkg_ll", " weight/20")
# bkg_tt_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_bkg_tt", " weight/20")
# sig_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_sig", " weight/20")
# sig_ll_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_sig_ll", " weight/20")
# sig_tt_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_sig_tt", " weight/20")
# total_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_total", " weight/20")
# tot_ll_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_tot_ll", " weight/20")
# tot_tt_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_tot_tt", " weight/20")
# qqzz_tree.Draw("probsig*2000/(probsig*2000+probbkg*100+probbkg_qq) >> im_qqzz", " weight/20")

#c1 = R.TCanvas("c1", "Stacked Histograms", 800, 600)
#c1.SetLogy()

# im_bkg.Scale(nb_bkg/im_bkg.Integral())
# im_bkg_ll.Scale(nb_bkg_ll/im_bkg_ll.Integral())
# im_bkg_tt.Scale(nb_bkg_tt/im_bkg_tt.Integral())
# im_sig.Scale(nb_sig/im_sig.Integral())
# im_sig_ll.Scale(nb_sig_ll/im_sig_ll.Integral())
# im_sig_tt.Scale(nb_sig_tt/im_sig_tt.Integral())
# im_total.Scale(nb_total/im_total.Integral())
# im_tot_ll.Scale(nb_tot_ll/im_tot_ll.Integral())
# im_tot_tt.Scale(nb_tot_tt/im_tot_tt.Integral())

# im_inter_ll.Add(im_tot_ll, im_bkg_ll, 1, -1)
# im_inter_ll.Add(im_inter_ll, im_sig_ll, 1, -1)
# im_inter_ll.Scale(-im_inter_ll.Integral()/im_inter_ll.Integral())

# im_inter_tt.Add(im_tot_tt, im_bkg_tt, 1, -1)
# im_inter_tt.Add(im_inter_tt, im_sig_tt, 1, -1)

# # data_obs.Add(im_bkg, im_sig_ll, 1, 1)
# # data_obs.Add(data_obs, im_sig_tt, 1, 1)
# # data_obs.Add(data_obs, im_inter_ll, 1, -1)
# # data_obs.Add(data_obs, im_inter_tt, 1, 1)

# # data_obs.Add(im_total, 1)
# im_inter_tt.Scale(-im_inter_tt.Integral()/im_inter_tt.Integral())

# im_all_bkgs.Add(im_bkg, im_sig_tt, 1, 1)

# data_obs.Add(im_all_bkgs, im_sig_ll, 1, 1)
# data_obs.Add(data_obs, im_inter_ll, 1, -1)
# data_obs.Add(data_obs, im_inter_tt, 1, -1)
# data_obs.Add(data_obs, im_qqzz, 1, 1)

# forinter_tt.Add(im_inter_tt, im_bkg, 1, 1)
# forsig.Add(im_sig_ll, im_sig_tt, 1, 1)
# im_sig.SetLineColor(2)
# im_sig.SetStats(0)
# im_sig.SetMaximum(55)
# im_sig.Draw("hist")
# im_sig.GetXaxis().SetTitle("m_4l(GeV)")

# data_obs.SetStats(0)
# data_obs.SetMaximum(20)
# data_obs.GetXaxis().SetTitle("D_gg")
# data_obs.Draw("error")

# im_total.SetFillColor(40)
# im_qqzz.SetFillColor(30)

# hs = R.THStack("hs", "Stacked Histograms")

# hs.Add(im_qqzz)
# hs.Add(im_total)
# hs.Draw("same hist")

# legend = R.TLegend(0.7, 0.7, 0.9, 0.9)
# legend.AddEntry(im_total, "gg->2e2mu s+b+i", "f")
# legend.AddEntry(im_qqzz, "qq->zz", "f")
# #legend.AddEntry(im_sig, "gg->h->2e2m", "l")
# legend.AddEntry(data_obs, "obs", "e")
# legend.Draw()

# c1.SaveAs("./stack.png")

# c2 = R.TCanvas("c2", "probsig*2000/(probsig*2000+probbkg*100+probbkg_qq)", 800, 600)

# #c2.SetLogy()
# #c2.SetLogx()

# im_sig.SetLineColor(2)
# im_sig.SetStats(0)
# im_sig.Scale(1/im_sig.Integral())
# im_sig.SetMaximum(0.4)
# im_sig.Draw("hist")

# im_qqzz.SetLineColor(4)
# im_qqzz.Scale(1/im_qqzz.Integral())
# im_qqzz.Draw("same hist")

# im_bkg.SetLineColor(3)
# im_bkg.Scale(1/im_bkg.Integral())
# im_bkg.Draw("same hist")

# legend1 = R.TLegend(0.7, 0.7, 0.9, 0.9)
# legend1.AddEntry(im_sig, "sig", "l")
# legend1.AddEntry(im_qqzz, "qq->zz", "l")
# legend1.AddEntry(im_bkg, "gg->2e2m /h", "l")
# legend1.Draw()

# c2.SaveAs("./com.png")



