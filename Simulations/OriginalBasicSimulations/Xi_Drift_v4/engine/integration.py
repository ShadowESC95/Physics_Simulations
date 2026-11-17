# engine/integration.py

import numpy as np

def rk4_step_enhanced(xi, chi, dt):
    """
    4th-order Runge-Kutta step for evolving xi field using chi as a coupling field.

    Args:
        xi (np.ndarray): Current Xi field.
        chi (np.ndarray): Coupled Chi field.
        dt (float): Time step.

    Returns:
        np.ndarray: Updated Xi field after one RK4 step.
    """

    def xi_rhs(xi_val, chi_val):
        lap_xi = (
            -4 * xi_val
            + np.roll(xi_val, 1, axis=0)
            + np.roll(xi_val, -1, axis=0)
            + np.roll(xi_val, 1, axis=1)
            + np.roll(xi_val, -1, axis=1)
        )
        return lap_xi + 0.1 * np.tanh(chi_val)

    k1 = xi_rhs(xi, chi)
    k2 = xi_rhs(xi + 0.5 * dt * k1, chi)
    k3 = xi_rhs(xi + 0.5 * dt * k2, chi)
    k4 = xi_rhs(xi + dt * k3, chi)

    return xi + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

