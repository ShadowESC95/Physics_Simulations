# interactions/coherence_entropy_coupling.py

import numpy as np

def compute_coherence_entropy_coupling(xi, chi, coupling_strength=1.0):
    """
    Computes a nonlinear coupling source term: λ·Ξ·(∇χ)^2
    
    Args:
        xi (np.ndarray): Entropy field Ξ(x)
        chi (np.ndarray): Coherence field χ(x)
        coupling_strength (float): λ coupling coefficient

    Returns:
        np.ndarray: Coupled source term for ∂Ξ/∂t
    """
    grad = np.gradient(chi)
    grad_sq = sum([g**2 for g in grad])
    return coupling_strength * xi * grad_sq

