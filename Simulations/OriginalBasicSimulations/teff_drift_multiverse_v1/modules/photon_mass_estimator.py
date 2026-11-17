import numpy as np

def estimate_photon_mass(teff_field, gradient_weight=0.001):
    dy, dx = np.gradient(teff_field)
    grad_sq = dx**2 + dy**2
    avg_grad_sq = np.mean(grad_sq)
    photon_mass = gradient_weight * np.sqrt(avg_grad_sq)
    return photon_mass
