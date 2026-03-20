#ifndef primary_generator_action_hh
#define primary_generator_action_hh

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4ParticleGun.hh"
#include "globals.hh"

class primary_generator_action : public G4VUserPrimaryGeneratorAction
{
  public:
    primary_generator_action();
    virtual ~primary_generator_action();

    virtual void GeneratePrimaries(G4Event*);

  private:
    G4ParticleGun* particle_gun;
};

#endif
