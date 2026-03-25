#include "primary_generator_action.hh"
#include "G4RunManager.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"
primary_generator_action::primary_generator_action() : G4VUserPrimaryGeneratorAction() {
  G4int n_particle = 1;
  particle_gun = new G4ParticleGun(n_particle);
  G4ParticleTable* table = G4ParticleTable::GetParticleTable();
  G4ParticleDefinition* particle = table->FindParticle("proton");
  particle_gun->SetParticleDefinition(particle);
  particle_gun->SetParticleMomentumDirection(G4ThreeVector(0., 0., 1.));
  particle_gun->SetParticleEnergy(4.*MeV);
}
primary_generator_action::~primary_generator_action() {
  delete particle_gun;
}
void primary_generator_action::GeneratePrimaries(G4Event* event) {
  particle_gun->SetParticlePosition(G4ThreeVector(0., 0., 0.*cm));
  particle_gun->GeneratePrimaryVertex(event);
}
