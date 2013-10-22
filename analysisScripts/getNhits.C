#include <TH1.h>
#include <TFile.h>
#include <TLegend.h>
#include <TTree.h>
#include <TGraph.h>
#include <TMultiGraph.h>
#include <TCanvas.h>
#include <fstream>
#include <vector>
#include <TMath.h>
#include "Root.hh"
#include "Run.hh"
#include "EV.hh"
#include "MC.hh"
#include <string>
void GetNhitsInWindow(char* pFile, TH1D* hist);
void NhitSpectrum(char* inputFile, char* outputFile,double setXMinValue,double setXMaxValue,double setYMinValue,double setYMaxValue,double xbinWidth,char* xTitle,char* yTitle)
{
  
  double doubleNumBins = (setXMaxValue-setXMinValue)/xbinWidth; //Calculate the number of bins as standard
  Int_t numBins = (Int_t) doubleNumBins; //Calculate the number of bins as an integer value

  TCanvas *c1=new TCanvas("c1");

  /********* Stitching the title names together */ 
  //char* graphTitle = ";";
  //char* graphPlusXTitle = str::strcat(graphTitle,xTitle);
  //char* allTitles = str::strcat(graphPlusXTitle,yTitle); 
  char* allTitles = ";";

  TH1D* histogram = new TH1D("pySNOt",allTitles,numBins,setXMinValue,setXMaxValue);

  GetNhitsInWindow(inputFile,histogram);
  histogram->SetLineColor(1);
  histogram->SetStats(0);
  histogram->SetMaximum(setYMaxValue);
  histogram->Draw();
  c1->Update();
  c1->SaveAs(outputFile);

}

void GetNhitsInWindow(char* pFile, TH1D* hist){
  TFile *file = new TFile(pFile);
  TTree *tree = (TTree *)file->Get("T");
  RAT::DS::Root *rds = new RAT::DS::Root();
  tree->SetBranchAddress("ds", &rds);

  // PMT Properties are contained in different tree
  TTree *runtree = (TTree *)file->Get( "runT");
  RAT::DS::Run *pmtds = new RAT::DS::Run();
  runtree->SetBranchAddress("run", &pmtds);
  runtree->GetEntry();
  
  for(int iLoop =0; iLoop < tree->GetEntries() ; iLoop++ ){
    tree->GetEntry( iLoop ); 
      int eventCounter = rds->GetEVCount();
      if( eventCounter == 0 ) continue;
      RAT::DS::EV *pev= rds->GetEV(0);
      Int_t PMThits = pev->GetPMTCalCount();
      hist->Fill(PMThits);
    }
}

int main(int argc, char* argv[])
{
  NhitSpectrum("/data/snoplus/jonesc/batch_output/C14/C14.root","/data/snoplus/jonesc/batch_output/C14/output.root",0.0,1000.0,0,1500,10,"xtitle","ytitle");	
}



