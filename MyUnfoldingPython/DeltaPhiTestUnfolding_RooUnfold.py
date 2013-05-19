import  ROOT
import sys
#sys.path.append('/grid_mnt/opt__sbg__data__safe1/cms/fhoehle/MyIPHC_Unfolding/MyUnfoldingPython/')
sys.path.append('/opt/sbg/data/safe1/cms/fhoehle/MyIPHC_Unfolding/UnfoldingIPHC')
#import myRooUnfold_cfi
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
import classy_unfold1d_InputsOutputs_cfi 
unfoldResult = classy_unfold1d_InputsOutputs_cfi.unfoldedResult() 
genDeltaPhi = classy_unfold1d_InputsOutputs_cfi.usedDeltaPhiGenHist()
recDeltaPhi = classy_unfold1d_InputsOutputs_cfi.usedDeltaPhiRecHist()
migMatrix = classy_unfold1d_InputsOutputs_cfi.usedMigrationMatrix()
bckgHist = classy_unfold1d_InputsOutputs_cfi.backgroundsHist()
dataBS = classy_unfold1d_InputsOutputs_cfi.usedDataBckSubtracted()
dataUsed = classy_unfold1d_InputsOutputs_cfi.usedData()
dataUsedNotScaled = dataUsed.Clone("dataUsedNotScaled")
dataBckgSubtracted = dataUsed.Clone("dataBckgSubtracted")
dataBckgSubtracted.Reset("ICEM")
dataBckgSubtracted.Add(dataUsed)
dataBckgSubtracted.Add(bckgHist,-1.0)
import PyRoot_Functions.MyHistFunctions_cfi as MyHistFunctions_cfi
#############################
responseMatrixT = transponseTH2(migMatrix)
response = RooUnfoldResponse("response","response")
response.Setup(None,None,responseMatrixT)
###
unfold = RooUnfoldTUnfold(response, dataBckgSubtracted)
hReco = unfold.Hreco()
MyHistFunctions_cfi.SetErrorsNormHist(hReco,"width")
hReco.Scale(1.0/hReco.Integral("width"))
can = makeCan("UnfoldingVsGen")
hReco.Draw()
MyHistFunctions_cfi.SetErrorsNormHist(genDeltaPhi,"width")
genDeltaPhi.SetLineColor(2)

genDeltaPhi.Draw("sames")
can.Update()
import PyRoot_Functions.StatBoxFunctions_cfi as StatBoxFunctions_cfi
StatBoxFunctions_cfi.StatBoxSameLineColor(genDeltaPhi)
unfoldResult.SetLineColor(3)
MyHistFunctions_cfi.SetErrorsNormHist(unfoldResult,"width")
unfoldResult.Scale(1.0/unfoldResult.Integral("width"))
unfoldResult.Draw("samesE");
StatBoxFunctions_cfi.StatBoxSameLineColor(unfoldResult)
can.Update()
can.Modified()

