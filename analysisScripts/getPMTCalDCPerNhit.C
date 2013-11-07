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
#include <string>
#include "Root.hh"
#include "Run.hh"
#include "EV.hh"
#include "MC.hh"
#include <string>

/* DO NOT REMOVE - This is a standard Member of pySNOT */
void MakeGraph(char* inputFile, char* outputFile,double setXMinValue,double setXMaxValue,double setYMinValue,double setYMaxValue,double xbinWidth,char* graphTitle,char* xTitle,char* yTitle);


/* Place Customised functions here */
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
      int doubleCounter = 0;

      for(int ipmt=0;ipmt<PMThits;++ipmt){
        //Retrieve the PMTTruth Information for QHS vs QHL
        RAT::DS::PMTCal *PMTCal = pev->GetPMTCal(ipmt);
        double_t qhs = PMTCal->GetsQHS();                                   
        double_t qhl = PMTCal->GetsQHL();                
	
	//Check to see if a PMT has been double hit
	if(qhl > qhs){
	  doubleCounter = doubleCounter + 1;
	}
	
      }//end of looping over all the PMTs in a given event
      
      hist->Fill(doubleCounter/1.0*PMThits);
      //std::cout << "Number of PMTs hit:" << PMThits << " Number of doubleCounts: " << doubleCounter << std::endl;
      
    }
}



/* DO NOT REMOVE - This is a standard Member of pySNOT */
int main(int argc, char* argv[])
{
  double xMin ;
  double xMax ;
  double xWidth ;
  double yMin ;
  double yMax ;
  
  xMin = strtod(argv[6],NULL);
  xMax = strtod(argv[7],NULL);
  xWidth = strtod(argv[8],NULL);
  yMin = strtod(argv[9],NULL);
  yMax = strtod(argv[10],NULL);

  std::cout << "pySNOt::Checking the Inputs" << std::endl;
  std::cout << "pySNOt::Input File" << std::endl;
  std::cout << argv[1] << std::endl;
  std::cout << "pySNOt::Output File" << std::endl;
  std::cout << argv[2] << std::endl;
  std::cout << "pySNOt::Graph Title" << std::endl;
  std::cout << argv[3] << std::endl;
  std::cout << "pySNOt::X Axis Title" << std::endl;
  std::cout << argv[4] << std::endl;
  std::cout << "pySNOt::y Axis Title" << std::endl;
  std::cout << argv[5] << std::endl;
  std::cout << "pySNOt::xLow" << std::endl;
  std::cout << xMin << std::endl;
  std::cout << "pySNOt::xHigh" << std::endl;
  std::cout << xMax << std::endl;
  std::cout << "pySNOt::xBinWidth" << std::endl;
  std::cout << argv[8] << std::endl;
  std::cout << "pySNOt::yLow" << std::endl;
  std::cout << argv[9] << std::endl;
  std::cout << "pySNOt::yHigh" << std::endl;
  std::cout << argv[10] << std::endl;

  MakeGraph(argv[1],argv[2],xMin,xMax,yMin,yMax,xWidth,argv[3],argv[4],argv[5]);	
}

/* DO NOT REMOVE - This is a standard Member of pySNOT */
void MakeGraph(char* inputFile, char* outputFile,double setXMinValue,double setXMaxValue,double setYMinValue,double setYMaxValue,double xbinWidth,char* graphTitle,char* xTitle,char* yTitle)
{
  
  double doubleNumBins = (setXMaxValue-setXMinValue)/xbinWidth; //Calculate the number of bins as standard
  Int_t numBins = (Int_t) doubleNumBins; //Calculate the number of bins as an integer value

  TCanvas *c1=new TCanvas("c1");

  /*This is required to make the Graph */
  char result[100];
  strcpy(result,graphTitle); //Copy graphTitle into the result string
  strcat(result,";");        //Append extra char* variables to this string 
  strcat(result,xTitle);
  strcat(result,";");
  strcat(result,yTitle);
  
  TH1D* histogram = new TH1D("pySNOt",result,numBins,setXMinValue,setXMaxValue);

  GetNhitsInWindow(inputFile,histogram);
  histogram->SetLineColor(1);
  histogram->SetStats(0);
  //histogram->SetMaximum(setYMaxValue);
  histogram->Draw();
  c1->Update();
  c1->SaveAs(outputFile);
}


