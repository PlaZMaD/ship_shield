#ifndef FLUXDET_H
#define FLUXDET_H

#include "Rtypes.h"                     // for ShipMuonShield::Class, Bool_t, etc
#include "FairDetector.h"
#include "TLorentzVector.h"
#include "fluxDetPoint.h"

class fluxDetPoint;
class FairVolume;
class TClonesArray;

class fluxDet : public FairDetector
{
 public:
 	fluxDet(const char* name, const char* Title, Bool_t Active, Double_t X, Double_t Y, Double_t Z, Double_t dX, Double_t dY, Double_t dZ);
 	fluxDet();
 	fluxDet(const char* name,Bool_t Active);
 	virtual ~fluxDet();
   virtual void   Initialize();
   
 	void ConstructGeometry();
 	virtual Bool_t ProcessHits( FairVolume* v=0);
 	virtual TClonesArray* GetCollection(Int_t iColl) const;
 	virtual void Reset();
 	void SetZposition(Double_t z) {fzPos = z;}
 	fluxDetPoint* AddHit(Int_t trackID, Int_t detID,
			 TVector3 pos, TVector3 mom,
			 Int_t pdgCode);

 	virtual void Register();
 	virtual void   EndOfEvent();
    virtual void   FinishPrimary() {;}
    virtual void   FinishRun() {;}
    virtual void   BeginPrimary() {;}
    virtual void   PostTrack() {;}
    virtual void   PreTrack() {;}
    virtual void   BeginEvent() {;}

 protected:
 	// createBox(TString voxName, TGeoMedium *medium, Double_t X, Double_t Y,  Double_t dZ);
 	/** Track information to be stored until the track leaves the active volume.*/
    Int_t          fTrackID;            //!  track index
    Int_t          fVolumeID;           //!  volume id
    TLorentzVector fPos;                //!  position at entrance
    TLorentzVector fMom;                //!  momentum at entrance

    /** Detector parameters.*/


    Double_t fxSize; //! width of the detector
    Double_t fySize; //! height of the detector
    Double_t fzSize; //! length of the detector



    Double_t fxCenter; //! x-position of the detector center
    Double_t fyCenter; //! y-position of the detector cente
    Double_t fzPos;     //!  z-position of flux plane			

    TGeoVolume* fDetector; // flux detector object

    /** container for data points */
    TClonesArray* ffluxDetPointCollection;

    Int_t InitMedium(const char* name);

    ClassDef(fluxDet,3)

};
#endif
