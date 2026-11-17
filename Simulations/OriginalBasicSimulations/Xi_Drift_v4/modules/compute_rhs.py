import numpy as np

def laplacian(field):
    return (
        -4 * field
        + np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
    )

def compute_rhs(xi, chi, lambda_coupling=0.3):
    """Right-hand side of the PDE: ∂Ξ/∂t = ∇²Ξ + λ Ξχ"""
    return laplacian(xi) + lambda_coupling * xi * chi

def rk4_step(xi, chi, dt, lambda_coupling=0.3):
    """One RK4 update step for Ξ"""
    k1 = compute_rhs(xi, chi, lambda_coupling)
    k2 = compute_rhs(xi + 0.5 * dt * k1, chi, lambda_coupling)
    k3 = compute_rhs(xi + 0.5 * dt * k2, chi, lambda_coupling)
    k4 = compute_rhs(xi + dt * k3, chi, lambda_coupling)

    return xi + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# Test RK4 on one step using the existing field
rk4_updated_xi = rk4_step(xi_field, chi_field, dt=0.01)
rk4_updated_xi.mean(), rk4_updated_xi.std()
