#include "stepping_action.hh"
#include "run_action.hh"
#include "G4Step.hh"
#include "G4SystemOfUnits.hh"
stepping_action::stepping_action(run_action* ra) : G4UserSteppingAction(), r_action(ra) {}
stepping_action::~stepping_action() {}
void stepping_action::UserSteppingAction(const G4Step* step) {
  G4double edep = step->GetTotalEnergyDeposit();
  if (edep <= 0.0) return;
  G4double z = step->GetPostStepPoint()->GetPosition().z();
  if (z >= 0.0 && z < 400.0*mm) {
    G4int bin = (G4int)(z / (4.0*mm));
    r_action->add_edep(bin, edep);
  }
}
