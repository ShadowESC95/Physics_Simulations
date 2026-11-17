
def photon_electron_interaction(photon_energy, electron_mass, coupling_constant):
    return photon_energy * coupling_constant / (electron_mass ** 0.5)

if __name__ == "__main__":
    photon_energy = 2.5  # in eV
    electron_mass = 9.11e-31  # in kg
    coupling_constant = 3.14  # dimensionless
    
    interaction_strength = photon_electron_interaction(photon_energy, electron_mass, coupling_constant)
    print(f"Photon-Electron Interaction Strength: {interaction_strength}")
