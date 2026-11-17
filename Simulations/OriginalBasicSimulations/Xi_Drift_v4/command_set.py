def laplacian(field):
    return (
        -4 * field
        + np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
    )

def compute_rhs(xi, chi, lambda_coupling=0.3):
    return laplacian(xi) + lambda_coupling * xi * chi

def rk4_step(xi, chi, dt, lambda_coupling=0.3):
    k1 = compute_rhs(xi, chi, lambda_coupling)
    k2 = compute_rhs(xi + 0.5 * dt * k1, chi, lambda_coupling)
    k3 = compute_rhs(xi + 0.5 * dt * k2, chi, lambda_coupling)
    k4 = compute_rhs(xi + dt * k3, chi, lambda_coupling)
    return xi + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def compute_rhs_curvature(xi, chi, lambda_coupling=0.3, curvature_coupling=0.1):
    lap_xi = laplacian(xi)
    lap_chi = laplacian(chi)
    return lap_xi + lambda_coupling * xi * chi + curvature_coupling * lap_chi * xi

def rk4_step_curvature(xi, chi, dt, lambda_coupling=0.3, curvature_coupling=0.1):
    k1 = compute_rhs_curvature(xi, chi, lambda_coupling, curvature_coupling)
    k2 = compute_rhs_curvature(xi + 0.5 * dt * k1, chi, lambda_coupling, curvature_coupling)
    k3 = compute_rhs_curvature(xi + 0.5 * dt * k2, chi, lambda_coupling, curvature_coupling)
    k4 = compute_rhs_curvature(xi + dt * k3, chi, lambda_coupling, curvature_coupling)
    return xi + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
