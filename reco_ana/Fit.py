import ROOT as R
import ctypes

fL = -0.5 - (-1)*0.23122
fR = - (-1)*0.23122

def Fit():

    #R.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")

    f_tot = R.TFile("gg2e2m_tot.root", "READ")
    f_bkg = R.TFile("gg2e2m_bkg.root", "READ")
    f_sig = R.TFile("gg2e2m_sig.root", "READ")

    tree_tot = f_tot.Get("Events")
    tree_bkg = f_bkg.Get("Events")
    tree_sig = f_sig.Get("Events")

    print("fL = {0} \n".format(fL))
    print("fR = {0} \n".format(fR))

    xmm = "1/8*((1+ 4*x*y + y^2+ x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1+4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*[0]"

    xmn = "1/8*((1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1+4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1-4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*[1]"

    xm0 = "-(-1+x^2*y^2)*((-0.26878)^2+(0.23122)^2)^2*[2]"

    x00 = "(-1+x^2)*(-1+y^2)*((-0.26878)^2+(0.23122)^2)^2*[3]"
    
    c1 = R.TCanvas("c1", " ", 800, 600)
    ca = R.TH2F("ca", " ", 10, -1, 1, 10, -1, 1)
    cb = R.TH2F("cb", " ", 10, -1, 1, 10, -1, 1)

    tree_sig.Draw("costheta1:costheta2>>cb", "", "lego")
    fitsig = R.TF2("fitsig", "(1e6*1/8*((1+ 4*x*y + y^2+ x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1+4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*[0]*1e-6 + \
          (-1 + x^2)*(-1 + y^2)*((-0.26878)^2 + (0.23122)^2)^2*[1])*3000", -1, 1, -1, 1)

    fitsig.SetParameters(0, 0.3)
    fitsig.SetParLimits(0, -1, 0.3)
    #fitsig.SetParameters(1, 10)
    cb.Scale(286.86/cb.Integral())
    cb.Fit("fitsig","WIDTH")
    cb.SetStats(0)
    cb.GetYaxis().SetTitle("cos#theta_{1}")
    cb.GetXaxis().SetTitle("cos#theta_{2}")
    fitsig.Draw("same lego")
    c1.SaveAs("./ctheta_sig.png")

    c2 = R.TCanvas("c2", " ", 800, 600)
    tree_bkg.Draw("costheta1:costheta2>>ca", "", "lego")
    fitbkg = R.TF2("fitbkg", "(1e3*1/8*((1+ 4*x*y + y^2+ x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1+4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*[0]*1e-3 + \
          1e3*1/8*((1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1+4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1-4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*[1]*1e-3+ \
          -1e3*(-1+x^2*y^2)*((-0.26878)^2+(0.23122)^2)^2*[2]*1e-3 + \
          1e3*(-1+x^2)*(-1+y^2)*((-0.26878)^2+(0.23122)^2)^2*[3]*1e-3)*3000", -1, 1, -1, 1)
    fitbkg.SetParameters(0, 0, 0, 0)
    ca.Scale(5328/ca.Integral())
    ca.Fit("fitbkg", "WIDTH")
    ca.SetStats(0)
    ca.GetYaxis().SetTitle("cos#theta_{1}")
    ca.GetXaxis().SetTitle("cos#theta_{2}")
    #ca.Draw("same")
    fitbkg.Draw("same lego")
    c2.SaveAs("./ctheta_bkg.png")

    c_fit = R.TCanvas("c_fit", " ", 800, 600)
    fit = R.TH2F("fit", " ", 50, -1, 1, 50, -1, 1)
    tree_tot.Draw("costheta1:costheta2>>fit", "", "COLZ")
    ffit = R.TF2("ffit", "(1e3*1/8*((1+ 4*x*y + y^2+ x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1+4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*309.781*1e-3 + \
          1e3*1/8*((1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1+4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1-4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*(-119.504)*1e-3+ \
          -1e3*(-1+x^2*y^2)*((-0.26878)^2+(0.23122)^2)^2*56.7074*1e-3 + \
          1e3*(-1+x^2)*(-1+y^2)*((-0.26878)^2+(0.23122)^2)^2*[0]*(-5.79)*1e-3 + \
          1e3*(-1+x^2)*(-1+y^2)*((-0.26878)^2+(0.23122)^2)^2*[0]^2*(7.34)*1e-3 + \
          1e3*(-1+x^2)*(-1+y^2)*((-0.26878)^2+(0.23122)^2)^2*65.14*1e-3)*3000", -1, 1, -1, 1)
    ffit.SetParameters(1)
    #ffit.SetParLimits(0, -1, 100)
    fit.Scale(5004/fit.Integral())
    fit.Fit("ffit")
    fit.SetStats(0)
    fit.GetYaxis().SetTitle("cos#theta_{1}")
    fit.GetXaxis().SetTitle("cos#theta_{2}")
    fit.Draw("same")
    ffit.Draw("same")
    c_fit.SaveAs("./ctheta_tot.png")

    c3 = R.TCanvas("c3", " ", 800, 600)

    test1 = R.TF2("test1", "1e3*1/8*((1+ 4*x*y + y^2+ x^2*(1+y^2))*(-0.26878)^4 + \
          2*(1-4*x*y+y^2+x^2*(1+y^2))*(-0.26878)^2*(0.23122)^2 + \
          (1+4*x*y+y^2+x^2*(1+y^2))*(0.23122)^4)*1e-3", -1, 1, -1, 1)
    test1.SetMinimum(0)
    #test1.SetMaximum(0.010)
    test1.Draw("LEGO")
    c3.SaveAs("./test1.png")

    c4 = R.TCanvas("c4", " ", 800, 600)
    test2 = R.TF2("test2", "-(-1+x^2*y^2)*((-0.26878)^2+(0.23122)^2)^2", -1, 1, -1, 1)
    test2.Draw("LEGO")
    c4.SaveAs("./test2.png")



if __name__ == "__main__":
    Fit()