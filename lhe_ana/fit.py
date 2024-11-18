import ROOT
import math

def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


file_data = ROOT.TFile.Open("forCombine_mh125.root")
file_ex = ROOT.TFile.Open("forCombine_mh130.root")

dir_data = file_data.Get("eemm")
h_data = dir_data.Get("data_obs")

dir_ex = file_ex.Get("eemm")
h_ex = dir_ex.Get("im_tot")

nll0 = 0
nll_pri = 0

nbin = h_data.GetNbinsX()
print(nbin)
for i in range(1, nbin+1):
    _i_pseudo_expect = h_data.GetBinContent(i)
    #_i_obs = round(h_data.GetBinContent(i))
    _i_obs = h_data.GetBinContent(i)
    _i_expect = h_ex.GetBinContent(i)
    #nll0 = (_i_obs * math.log(_i_pseudo_expect) - _i_pseudo_expect - math.log(factorial_iterative(_i_obs))) + nll0
    #nll0 = math.log(ROOT.TMath.Poisson(_i_obs, _i_pseudo_expect)) + nll0
    if _i_expect >= 20:
        nll0 = math.log(ROOT.TMath.Gaus(_i_obs, _i_pseudo_expect, math.sqrt(_i_pseudo_expect), True)) + nll0
    else:
        nll0 = math.log(ROOT.TMath.Poisson(_i_obs, _i_pseudo_expect)) + nll0
    #nll_pri = (_i_obs * math.log(_i_expect) - _i_expect - math.log(factorial_iterative(_i_obs))) + nll_pri
    nll_pri =1

print("nll0: ", nll0, " nll_prime: ", nll_pri)
print("nll_prime-nll0 = ", -2*(nll_pri-nll0))

# c1 = ROOT.TCanvas("c1", "Quartic Fit with Extremum Constraint", 800, 600)


# graph = ROOT.TGraph(5)
# points = [(50/125, 2.1858), (150/125, 2.192), (1, 0), (100/125, 2.8822), (80/125, 1.89364), (130/125, 2.60), (140/125, 1.7836), (160/125, 0.75)]

# for i, (x, y) in enumerate(points):
#     graph.SetPoint(i, x, y)


# graph.SetMarkerStyle(20)
# graph.SetMarkerSize(1)
# graph.SetTitle(" ")


# # fit_function = ROOT.TF1("fit_function", "[0]*(x - 1)**2 * (x**2 + [1]*x + [2])", 0, 1.5)

# # fit_function.SetParameters(1, 0, 0)

# # graph.Fit(fit_function, "R")
# graph.GetXaxis().SetTitle('mh/125')
# graph.GetYaxis().SetTitle('-2#Delta log')

# graph.Draw("AP")

# c1.SaveAs("./fit.png")

