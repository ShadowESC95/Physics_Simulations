# interactions/entropy_geometry_coupling.py

import numpy as np

def compute_entropy_geometry_coupling(entropy_field, ricci_scalar, xi_field, alpha=1.0):
    """
    Compute the entropy–geometry coupling term from the variation δ(Ξ·R).
    
    Parameters:
        entropy_field (ndarray): Ξ(x, y, z, t) entropy scalar field
        ricci_scalar (ndarray): R(x, y, z, t) Ricci scalar from geometry_curvature
        xi_field (ndarray): Ξ(x, y, z, t) entropy field again (for sanity check)
        alpha (float): coupling constant λ_ΞG
    
    Returns:
        ndarray: Coupled source term for Ξ evolution equation
    """
    assert entropy_field.shape == ricci_scalar.shape == xi_field.shape
    return alpha * entropy_field * ricci_scalar

