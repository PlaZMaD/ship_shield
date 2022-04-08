#include "fluxDetPoint.h"

#include <iostream>
using std::cout;
using std::endl;


fluxDetPoint::fluxDetPoint()
  : FairMCPoint()
{
}

fluxDetPoint::fluxDetPoint(Int_t trackID, Int_t detID,
			   TVector3 pos, TVector3 mom, Int_t pdgcode)
  : FairMCPoint(trackID, detID, pos, mom, 0, 0, 0), fPdgCode(pdgcode)
{
}
// -------------------------------------------------------------------------

// -----   Destructor   ----------------------------------------------------
fluxDetPoint::~fluxDetPoint() { }
// -------------------------------------------------------------------------

// -----   Public method Print   -------------------------------------------
void fluxDetPoint::Print() const
{
  cout << "-I- fluxDetPoint: veto point for track " << fTrackID
       << " in detector " << fDetectorID << endl;
  cout << "    Position (" << fX << ", " << fY << ", " << fZ
       << ") cm" << endl;
  cout << "    Momentum (" << fPx << ", " << fPy << ", " << fPz
       << ") GeV" << endl;
}
// -------------------------------------------------------------------------

ClassImp(fluxDetPoint)
