// run_action.cc — modified for Bethe-Bloch study
// Prints particle label in header so Python can parse multiple runs

#include "run_action.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleDefinition.hh"
#include "primary_generator_action.hh"

run_action::run_action() : G4UserRunAction(), edeps(100, 0.0) {}
run_action::~run_action() {}

void run_action::BeginOfRunAction(const G4Run*) {
  for (auto& e : edeps) e = 0.0;
}

void run_action::EndOfRunAction(const G4Run* run) {
  G4int events = run->GetNumberOfEvent();
  if (events == 0) return;

  // Get particle info for labelling
  const auto* gun = static_cast<const primary_generator_action*>(
    G4RunManager::GetRunManager()->GetUserPrimaryGeneratorAction());

  G4String pname = "unknown";
  G4double energy_MeV = 0;
  G4int    charge = 1;

  if (gun) {
    auto* pg = gun->GetParticleGun();
    pname      = pg->GetParticleDefinition()->GetParticleName();
    energy_MeV = pg->GetParticleEnergy() / MeV;
    charge     = (G4int)pg->GetParticleDefinition()->GetPDGCharge();
  }

  // Header line — parsed by Python
  G4cout << "=== BRAGG DATA: particle=" << pname
         << " energy=" << energy_MeV << "MeV"
         << " z=" << charge << " ===" << G4endl;

  for (G4int i = 0; i < 100; i++) {
    G4cout << "depth: " << (i + 0.5) * 4.0
           << " mm, edep: " << edeps[i] / events / keV
           << " keV/event" << G4endl;
  }
}
