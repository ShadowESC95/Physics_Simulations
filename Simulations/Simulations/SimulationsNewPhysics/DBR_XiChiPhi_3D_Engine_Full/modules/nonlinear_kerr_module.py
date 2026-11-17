
import numpy as np

def apply_kerr_nonlinearity(epsilon, E_field, chi3=0.01):
    intensity = np.sum(E_field**2, axis=-1)
    for d in range(3):
        epsilon[..., d] += chi3 * intensity
    return epsilon
