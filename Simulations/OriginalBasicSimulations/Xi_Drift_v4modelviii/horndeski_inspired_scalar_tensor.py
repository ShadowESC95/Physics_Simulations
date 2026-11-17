# Implement Model 4: Horndeski-inspired scalar-tensor cosmology using Ξ
def model4_rhs(xi, chi, curvature_coeff=0.2, lambda_coupling=0.3):
    """
    Horndeski-inspired approximation:
    ∂Ξ/∂t = ∇²Ξ + λ Ξχ + ξ R Ξ^2
    where R is approximated by ∇²(χ) as a curvature proxy
    """
    lap_xi = laplacian(xi)
    lap_chi = laplacian(chi)
    curvature_term = curvature_coeff * lap_chi * xi**2  # approximated R Ξ^2 term
    return lap_xi + lambda_coupling * xi * chi + curvature_term

def rk4_step_model4(xi, chi, dt, lambda_coupling=0.3, curvature_coeff=0.2):
    k1 = model4_rhs(xi, chi, curvature_coeff, lambda_coupling)
    k2 = model4_rhs(xi + 0.5 * dt * k1, chi, curvature_coeff, lambda_coupling)
    k3 = model4_rhs(xi + 0.5 * dt * k2, chi, curvature_coeff, lambda_coupling)
    k4 = model4_rhs(xi + dt * k3, chi, curvature_coeff, lambda_coupling)
    return xi + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# Run one RK4 step of Model 4
xi_model4 = rk4_step_model4(xi_field.copy(), chi_field.copy(), dt=0.01)
xi_model4.mean(), xi_model4.std()
