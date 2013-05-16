import  ROOT
import sys
sys.path.append('/grid_mnt/opt__sbg__data__safe1/cms/fhoehle/MyIPHC_Unfolding/MyUnfoldingPython/')
import myRooUnfold_cfi
ROOT.gROOT.LoadMacro( "/grid_mnt/opt__sbg__data__safe1/cms/fhoehle/MySoftware/RooUnfold-1.1.1/libRooUnfold.so" )
from ROOT import RooUnfoldResponse
from ROOT import RooUnfold
from ROOT import RooUnfoldBayes
from ROOT import RooUnfoldSvd
from ROOT import RooUnfoldTUnfold
def transponseTH2(h2):
  yAxis = h2.GetYaxis(); nBinsY = h2.GetNbinsY()
  xAxis = h2.GetXaxis(); nBinsX = h2.GetNbinsX()
  h2T = ROOT.TH2F(h2.GetName()+"_transposed",h2.GetName()+"_tranposed", nBinsY ,yAxis.GetXmin(),yAxis.GetXmax(), nBinsX ,xAxis.GetXmin(),xAxis.GetXmax())
  for i in range(nBinsY +2):
    for j in range(nBinsX +2):
      h2T.SetBinContent(i,j,h2.GetBinContent(j,i))
      h2T.SetBinError(i,j,h2.GetBinError(j,i))
  return h2T
##reading matrix and data inputs
migmatrixFile = ROOT.TFile("../Unfolding/OwnMigMatrix.root")
responseMatrix = migmatrixFile.Get("migmatrix;1")
dataFile = ROOT.TFile("../Unfolding/DataToBeUnfoded.root")
data = dataFile.Get("hdataunwrapped;1")
##### bkg inputs
import bckgHist_cfi
##### substract background
dataBckgSubtracted = data.Clone("dataBckgSubtracted")
dataBckgSubtracted.Reset("ICEM")
dataBckgSubtracted.Add(data)
dataBckgSubtracted.Add(bckgHist_cfi.bckgHist,-1.0)
print "==================================== TRAIN ===================================="
response1= RooUnfoldResponse (10,0.0, 3.14,5,0.0,3.14);
response1.Setup(None,None,responseMatrix)
response2 = RooUnfoldResponse("response2","response2")
response2.Setup(None,None,responseMatrix)
response3 = RooUnfoldResponse(10,0.0,3.14,5,0.0,3.14);
responseMatrixT = transponseTH2(responseMatrix)
response3.Setup(None,None,responseMatrixT)
response4 = RooUnfoldResponse("response4","response4")
response4.Setup(None,None,responseMatrixT)

#print "==================================== UNFOLD ==================================="
#unfold= RooUnfoldBayes     (response1, data, 4);    #  OR
#unfold= RooUnfoldSvd     (response3, data, 3);   #  OR
unfold= RooUnfoldTUnfold (response3, data);
unfoldSub = RooUnfoldTUnfold(response4, dataBckgSubtracted)
hRecoSub = unfoldSub.Hreco()
hRecoSub.Scale(1.0/hRecoSub.Integral("width"))

#
hReco= unfold.Hreco();
unfold.Impl().RegularizeBins(1,1,5,ROOT.TUnfold.kRegModeCurvature)
hReco= unfold.Hreco();
#unfold.PrintTable (cout, hTrue);
hReco.Draw();
#hMeas.Draw("SAME");
#hTrue.SetLineColor(8);
#hTrue.Draw("SAME");
