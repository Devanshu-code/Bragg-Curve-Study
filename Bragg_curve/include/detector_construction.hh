#ifndef detector_construction_hh
#define detector_construction_hh

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"

class detector_construction : public G4VUserDetectorConstruction
{
  public:
    detector_construction();
    virtual ~detector_construction();

    virtual G4VPhysicalVolume* Construct();
    virtual void ConstructSDandField();
};

#endif
