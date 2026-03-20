#include "detector_construction.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"

detector_construction::detector_construction() : G4VUserDetectorConstruction() {}
detector_construction::~detector_construction() {}

G4VPhysicalVolume* detector_construction::Construct() {
  G4NistManager* nist = G4NistManager::Instance();
  G4Material* air = nist->FindOrBuildMaterial("G4_AIR");
  G4Material* argon = nist->FindOrBuildMaterial("G4_Ar");

  G4Box* world_box = new G4Box("world", 20*cm, 20*cm, 50*cm);
  G4LogicalVolume* world_log = new G4LogicalVolume(world_box, air, "world");
  G4VPhysicalVolume* world_phys = new G4PVPlacement(0, G4ThreeVector(), world_log, "world", 0, false, 0);

  G4Box* gas_box = new G4Box("gas", 10*cm, 10*cm, 20*cm);
  G4LogicalVolume* gas_log = new G4LogicalVolume(gas_box, argon, "gas");
  new G4PVPlacement(0, G4ThreeVector(0, 0, 20*cm), gas_log, "gas", world_log, false, 0);

  return world_phys;
}

void detector_construction::ConstructSDandField() {}
