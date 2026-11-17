# interactions/electromagnetic_fields.py

import numpy as np

def compute_electric_magnetic_fields(A_mu):
    """
    Compute electric and magnetic field components from Aμ.
    Aμ = (A0, A1, A2, A3), assumes Cartesian lattice.

    Returns:
        tuple of np.ndarray: (E_field, B_field)
            Each with shape (x, y, z, 3)
    """
    A0, Ax, Ay, Az = A_mu[..., 0], A_mu[..., 1], A_mu[..., 2], A_mu[..., 3]
    grad_0 = np.gradient(A0)
    grad_x = np.gradient(Ax)
    grad_y = np.gradient(Ay)
    grad_z = np.gradient(Az)

    # Electric field E = -∇A0 - ∂A⃗/∂t (here ∂t ~ 0, only spatial)
    E_field = np.stack([-grad_0[0], -grad_0[1], -grad_0[2]], axis=-1)

    # Magnetic field B = ∇ × A⃗
    curl_x = grad_y[2] - grad_z[1]
    curl_y = grad_z[0] - grad_x[2]
    curl_z = grad_x[1] - grad_y[0]
    B_field = np.stack([curl_x, curl_y, curl_z], axis=-1)

    return E_field, B_field

def compute_lorentz_scalar(E, B):
    """
    Compute E² - B² Lorentz scalar.
    """
    E2 = np.sum(E**2, axis=-1)
    B2 = np.sum(B**2, axis=-1)
    return E2 - B2

