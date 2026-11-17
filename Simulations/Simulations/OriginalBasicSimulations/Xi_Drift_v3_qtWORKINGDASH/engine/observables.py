import numpy as np

def check_symmetry(field):
    """Checks basic left-right symmetry"""
    flipped = np.flip(field, axis=1)
    return np.allclose(field, flipped, atol=1e-3)

def compute_conserved_quantity(xi, chi):
    """Example: Ξχ interaction Hamiltonian energy density"""
    interaction = xi * chi
    return np.sum(interaction)
