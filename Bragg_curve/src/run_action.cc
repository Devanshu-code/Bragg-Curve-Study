#include "run_action.hh"
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4SystemOfUnits.hh"
run_action::run_action() : G4UserRunAction(), edeps(100, 0.0) {}
run_action::~run_action() {}
void run_action::BeginOfRunAction(const G4Run*) {
  for (auto& edep : edeps) edep = 0.0;
}
void run_action::EndOfRunAction(const G4Run* run) {
  G4int events = run->GetNumberOfEvent();
  if (events == 0) return;
  G4cout << "--- bragg curve results ---" << G4endl;
  for (G4int i = 0; i < 100; i++) {
    G4cout << "depth: " << (i + 0.5) * 4.0 << " mm, edep: " << edeps[i]/events/keV << " keV/event" << G4endl;
  }
}
