#ifndef fluxDetHIT_H
#define fluxDetHIT_H 1
#include "FairVolume.h"
#include "ShipHit.h"
#include "fluxDetPoint.h"
#include "TObject.h"
#include "TGeoShape.h"
#include "TGeoPhysicalNode.h"


class fluxDetHit : public ShipHit
{
  public:

    /** Default constructor **/
    fluxDetHit();

    /** Constructor from fluxDetHit
     *@param detID    Detector ID
     *@param t_1, t_2      TDC on both sides
     *@param flag      True/False, in case of pile up
     **/
//    fluxDetHit(TimeDetPoint* p, Double_t t0);

    /** Destructor **/
    virtual ~fluxDetHit();

    /** Accessors **/
    Double_t GetX();
    Double_t GetY();
    Double_t GetZ();
    TVector3 GetXYZ();
    TGeoNode* GetNode();
    // std::vector<double> GetTime(Double_t x);
    // std::vector<double> GetTime();
    // std::vector<double> GetMeasurements();
    // std::vector<double> GetMeasurements();
    /** Modifier **/
    // void SetTDC(Float_t val1, Float_t val2){t_1=val1;t_2=val2;}

    /** Output to screen **/
    virtual void Print() const;

    // Double_t Resol(Double_t x);
    // void setInvalid() {flag = false;}
    // void setIsValid() {flag = true;}
    // bool isValid() const {return flag;}
  private:
    fluxDetHit(const fluxDetHit& point);
    fluxDetHit operator=(const fluxDetHit& point);


    ClassDef(fluxDetHit,1);

};

#endif
