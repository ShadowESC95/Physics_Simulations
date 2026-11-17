import numpy as np

def compute_stueckelberg_term(phi_field, gauge_field, coupling_constant=1.0, spacing=None):
    """
    Computes the Stueckelberg mass term: (Aμ - ∂μφ)^2
    Assumes phi_field is 4D (t, x, y, z) and gauge_field is 5D (t, x, y, z, mu)
    
    Args:
        phi_field (ndarray): Real scalar field φ(t,x,y,z)
        gauge_field (ndarray): Gauge field Aμ with shape (..., 4)
        coupling_constant (float): m_A^2 coefficient
        spacing (tuple or None): Grid spacing for each axis (dt, dx, dy, dz)
    
    Returns:
        ndarray: Scalar Stueckelberg mass term field
    """
    if phi_field.ndim != 4:
        raise ValueError(f"Expected 4D phi_field, got {phi_field.ndim}D")

    # Gradient: returns list of 4 arrays [∂tφ, ∂xφ, ∂yφ, ∂zφ]
    grad_phi = np.gradient(phi_field, *spacing) if spacing else np.gradient(phi_field)

    if len(grad_phi) != 4:
        raise ValueError(f"Expected 4 gradient components (t,x,y,z), got {len(grad_phi)}")

    # Stack into shape (..., 4) to match gauge_field
    grad_phi_stacked = np.stack(grad_phi, axis=-1)

    if gauge_field.shape != grad_phi_stacked.shape:
        raise ValueError(f"Shape mismatch: gauge_field {gauge_field.shape}, ∂μφ {grad_phi_stacked.shape}")

    A_minus_dphi = gauge_field - grad_phi_stacked
    squared_term = np.sum(A_minus_dphi**2, axis=-1)

    return 0.5 * coupling_constant * squared_term

