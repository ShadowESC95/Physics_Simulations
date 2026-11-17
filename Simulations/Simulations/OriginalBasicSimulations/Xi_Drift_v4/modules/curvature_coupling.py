# Provide full upgraded Ξ evolution logic including curvature coupling
def compute_rhs_curvature(xi, chi, lambda_coupling=0.3, curvature_coupling=0.1):
    """
    Right-hand side of Ξ PDE with curvature coupling:
    ∂Ξ/∂t = ∇²Ξ + λ Ξχ + ξ (∇²χ) Ξ
    """
    lap_xi = laplacian(xi)
    lap_chi = laplacian(chi)
    return lap_xi + lambda_coupling * xi * chi + curvature_coupling * lap_chi * xi

def rk4_step_curvature(xi, chi, dt, lambda_coupling=0.3, curvature_coupling=0.1):
    """Runge-Kutta 4th order step for Ξ with curvature coupling"""
    k1 = compute_rhs_curvature(xi, chi, lambda_coupling, curvature_coupling)
    k2 = compute_rhs_curvature(xi + 0.5 * dt * k1, chi, lambda_coupling, curvature_coupling)
    k3 = compute_rhs_curvature(xi + 0.5 * dt * k2, chi, lambda_coupling, curvature_coupling)
    k4 = compute_rhs_curvature(xi + dt * k3, chi, lambda_coupling, curvature_coupling)

    return xi + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# Perform a curvature-coupled RK4 step
rk4_curved_xi = rk4_step_curvature(xi_field, chi_field, dt=0.01)
rk4_curved_xi.mean(), rk4_curved_xi.std()
