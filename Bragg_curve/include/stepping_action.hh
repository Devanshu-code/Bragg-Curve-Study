#ifndef stepping_action_hh
#define stepping_action_hh
#include "G4UserSteppingAction.hh"
#include "globals.hh"
class run_action;
class stepping_action : public G4UserSteppingAction {
public:
  stepping_action(run_action*);
  virtual ~stepping_action();
  virtual void UserSteppingAction(const G4Step*);
private:
  run_action* r_action;
};
#endif
