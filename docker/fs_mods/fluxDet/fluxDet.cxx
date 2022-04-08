#include "fluxDet.h"
#include "fluxDetPoint.h"
#include "FairVolume.h"
#include "FairGeoVolume.h"
#include "FairGeoNode.h"
#include "FairRootManager.h"
#include "FairGeoLoader.h"
#include "FairGeoInterface.h"
#include "FairGeoMedia.h"
#include "FairGeoBuilder.h"
#include "FairRun.h"
#include "FairRuntimeDb.h"
#include "ShipDetectorList.h"
#include "ShipStack.h"

#include "TClonesArray.h"
#include "TVirtualMC.h"
#include "TGeoManager.h"
#include "TGeoBBox.h"
#include "TGeoCompositeShape.h"
#include "TGeoTube.h"
#include "TGeoMaterial.h"
#include "TGeoMedium.h"
#include "TMath.h" 
#include "TParticle.h" 
#include "TVector3.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>


fluxDet::fluxDet(const char* name, const char* Title, Bool_t Active, Double_t X, Double_t Y,Double_t Z, Double_t dX, Double_t dY, Double_t dZ)
	: FairDetector(name, Active, kfluxDet),
	  fTrackID(-1),
      fVolumeID(-1),
      fPos(TLorentzVector(X, Y, Z, 0.)),
      fMom(TLorentzVector (0., 0., 0., 0.)),
      fzPos(Z),
      fxSize(dX),
      fySize(dY),
      fzSize(dZ),
      fxCenter(X),
      fyCenter(Y),
      fDetector(0),
      ffluxDetPointCollection(new TClonesArray("fluxDetPoint"))
{
	// FairDetector::Initialize();
	// fPos = TLorentzVector (X, Y, Z, 0.);

}

fluxDet::fluxDet()
	: FairDetector("fluxDet", kTRUE, kfluxDet),
	  fTrackID(-1),
      fVolumeID(-1),
      fPos(TLorentzVector(0., 0., -3351, 0.)),
      fMom(TLorentzVector (0., 0., 0., 0.)),
      fzPos(-3350.),
      fxSize(450.),
      fySize(450.),
      fzSize(0.5),
      fxCenter(0.),
      fyCenter(0.),
      fDetector(0),
      ffluxDetPointCollection(new TClonesArray("fluxDetPoint"))
{
	// FairDetector::Initialize();
	// fPos = TLorentzVector (X, Y, Z, 0.);

}

fluxDet::fluxDet(const char* name,Bool_t Active)
	: FairDetector(name, Active, kfluxDet),
	  fTrackID(-1),
      fVolumeID(-1),
      fPos(TLorentzVector(0., 0., -3350, 0.)),
      fMom(TLorentzVector (0., 0., 0., 0.)),
      fzPos(-3350.),
      fxSize(450.),
      fySize(450.),
      fzSize(0.5),
      fxCenter(0.),
      fyCenter(0.),
      fDetector(0),
      ffluxDetPointCollection(new TClonesArray("fluxDetPoint"))
{
	// FairDetector::Initialize();


}
void fluxDet::Initialize()
{
  FairDetector::Initialize();
}

fluxDet::~fluxDet()
{
  if (ffluxDetPointCollection) {
    ffluxDetPointCollection->Delete();
    delete ffluxDetPointCollection;
  }
}

Int_t fluxDet::InitMedium(const char* name)
{
  
   static FairGeoLoader *geoLoad=FairGeoLoader::Instance();
   static FairGeoInterface *geoFace=geoLoad->getGeoInterface();
   static FairGeoMedia *media=geoFace->getMedia();
   static FairGeoBuilder *geoBuild=geoLoad->getGeoBuilder();

   FairGeoMedium *ShipMedium=media->getMedium(name);

   if (!ShipMedium)
   {
     Fatal("InitMedium","Material %s not defined in media file.", name);
     return -1111;
   }
   TGeoMedium* medium=gGeoManager->GetMedium(name);
   if (medium!=NULL)
     return ShipMedium->getMediumIndex();

   return geoBuild->createMedium(ShipMedium);
  
  return 0;
}

void fluxDet::EndOfEvent()
{
  ffluxDetPointCollection->Clear();
}



void fluxDet::Register()
{

  /** This will create a branch in the output tree called
      fluxDetPoint, setting the last parameter to kFALSE means:
      this collection will not be written to the file, it will exist
      only during the simulation.
  */

  FairRootManager::Instance()->Register("fluxDetPoint", "fluxDet",
                                        ffluxDetPointCollection, kTRUE);
}


TClonesArray* fluxDet::GetCollection(Int_t iColl) const
{
  if (iColl == 0) { return ffluxDetPointCollection; }
  else { return NULL; }
}



void fluxDet::Reset()
{
  ffluxDetPointCollection->Clear();
}


void fluxDet::ConstructGeometry()
{
  TGeoVolume *top = gGeoManager->GetTopVolume();
  
  InitMedium("vacuums");
  TGeoMedium *vacuums =gGeoManager->GetMedium("vacuums");
  
  ///////////////////////////////////////////////////////


  fDetector = gGeoManager->MakeBox("fluxDet", vacuums, fxSize, fySize, fzSize);
  fDetector->SetLineColor(kBlue);
  AddSensitiveVolume(fDetector);
  top->AddNode(fDetector, 1, new TGeoTranslation(0,0,fzPos));

  ///////////////////////////////////////////////////////

  return;
}


fluxDetPoint* fluxDet::AddHit(Int_t trackID, Int_t detID, TVector3 pos, TVector3 mom, Int_t pdgCode)
{
  TClonesArray& clref = *ffluxDetPointCollection;
  Int_t size = clref.GetEntriesFast();
  // cout << "veto hit called "<< pos.z()<<endl;
  return new(clref[size]) fluxDetPoint(trackID, detID, pos, mom, pdgCode);
}


Bool_t  fluxDet::ProcessHits(FairVolume* vol)
{
  /** This method is called from the MC stepping */
  //Set parameters at entrance of volume. Reset ELoss.
  if ( gMC->IsTrackEntering() ) {
    gMC->TrackPosition(fPos);
    gMC->TrackMomentum(fMom);
    fTrackID  = gMC->GetStack()->GetCurrentTrackNumber();
    TParticle* p = gMC->GetStack()->GetCurrentTrack();
    Int_t pdgCode = p->GetPdgCode();
    Int_t uniqueId;
    gMC->CurrentVolID(uniqueId);

  

	AddHit(fTrackID, uniqueId, TVector3(fPos.X(), fPos.Y(),  fPos.Z()), TVector3(fMom.Px(), fMom.Py(), fMom.Pz()), pdgCode);
	// Increment number of flux det points in TParticle
	ShipStack* stack = (ShipStack*) gMC->GetStack();
	stack->AddPoint(kfluxDet);

  }
  return kTRUE;

}

ClassImp(fluxDet)
