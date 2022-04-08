#include "fluxDetHit.h"
#include "fluxDet.h"
#include "TVector3.h"
#include "TMath.h"
#include "TRandom1.h"
#include "TRandom3.h"
#include "TGeoManager.h"
#include "TGeoBBox.h"
#include "TGeoNode.h"

#include <iostream>
#include <math.h>

using std::cout;
using std::endl;

Double_t speedOfLight = TMath::C() *100./1000000000.0 ; // from m/sec to cm/ns


// -----   Default constructor   --------------
fluxDetHit::fluxDetHit()
  : ShipHit()
{
 // flag = true;
}


// -----   Destructor   -------------------------
fluxDetHit::~fluxDetHit() { }


// ---- return mean time information
// std::vector<double>  fluxDetHit::Getflux(){
//      TGeoBBox* shape =  (TGeoBBox*)gGeoManager->GetVolume("fluxDet")->GetShape();
//      Double_t t0  =  (t_1+t_2)/2.-shape->GetDX()/v_drift;
//      Float_t lpos, lneg;
//      lneg = (t_1-t0)*v_drift;
//      lpos = (t_2-t0)*v_drift;
//      Float_t r1 = Resol(lneg);
//      Float_t r2 = Resol(lpos);
//      Double_t dt =  TMath::Sqrt(r1*r1+r2*r2);
//      std::vector<double> m;
//      m.push_back(t0);
//      m.push_back(dt);
//      return m;
// }
// -----   resolution function-------------------
// Double_t fluxDetHit::Resol(Double_t x)
// {
//   return par[0]*TMath::Exp( (x-par[2])/par[1] )+par[3]; 
// }

// std::vector<double> fluxDetHit::GetMeasurements(){
//  std::vector<double> m;
//  m.push_back( t_1);
//  m.push_back( t_2);
//  return m;
// }


// ----------------------------------------------
TVector3 fluxDetHit::GetXYZ()
{
    TGeoNavigator* nav = gGeoManager->GetCurrentNavigator();
    TGeoNode* node = GetNode();
    TGeoBBox* shape =  (TGeoBBox*)node->GetVolume()->GetShape();
    Double_t origin[3] = {shape->GetOrigin()[0],shape->GetOrigin()[1],shape->GetOrigin()[2]};
    Double_t master[3] = {0,0,0};
    nav->LocalToMaster(origin,master);
    TVector3 pos = TVector3(master[0],master[1],master[2]);
    return pos;
}


Double_t fluxDetHit::GetX()
{ TVector3 pos = GetXYZ();
  return pos.X();
}


Double_t fluxDetHit::GetY()
{ TVector3 pos = GetXYZ();
  return pos.Y();
}


Double_t fluxDetHit::GetZ()
{ TVector3 pos = GetXYZ();
  return pos.Z();
}

// Double_t fluxDetHit::GetPDG()
// { TVector3 pos = GetXYZ();
//   return pos.Z();
// }

TGeoNode* fluxDetHit::GetNode()
{
   TGeoNavigator* nav = gGeoManager->GetCurrentNavigator();
   TString path = "/flux Detector_1/fluxDet_";path+=fDetectorID;
   Bool_t rc = nav->cd(path);
   return nav->GetCurrentNode();
} 


// -----   Public method Print   -----------------------
void fluxDetHit::Print() const
{ 
  cout << "-I- fluxDetHit: fluxDet hit " << " in detector " << fDetectorID << endl;
}


// -----------------------------------------------------
ClassImp(fluxDetHit)

