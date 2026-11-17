# observables/observables.py
import numpy as np
from dolfinx import fem

def compute_fields(Xi: fem.Function, Chi: fem.Function,
                  Xi_dot: np.ndarray = None, Chi_dot: np.ndarray = None,
                  alpha=1.0, gamma=1.0, delta=-1.0, kappa=1.0):
    """
    Compute emergent E and B fields and other observables from Ξ, χ and their time derivatives.
    Xi_dot, Chi_dot are optional arrays of time derivatives at the current time.
    Returns dictionaries for E, B field components on mesh points, and scalars like rho_eff.
    """
    V = Xi.function_space
    mesh = V.mesh

    # Compute gradients of Xi and χ at cell centers or nodal points
    grad_Xi = fem.grad(Xi)
    grad_Chi = fem.grad(Chi)
    # Evaluate gradients on mesh points (this yields an array of shape (n_points, dim))
    grad_Xi_vals = grad_Xi.compute_point_values()
    grad_Chi_vals = grad_Chi.compute_point_values()

    # Compute A = kappa * χ * grad(Ξ) + alpha * grad(χ)
    A_vec = kappa * (Chi.x.array[:, None] * grad_Xi_vals) + alpha * grad_Chi_vals

    # If time derivatives are provided, compute Phi = gamma * Ξ + delta * Chi_dot
    if Xi_dot is not None and Chi_dot is not None:
        Phi_val = gamma * Xi.x.array + delta * Chi_dot
    else:
        # If not provided, assume Chi_dot ~ 0 for now
        Phi_val = gamma * Xi.x.array

    # Compute E = -∇Φ - ∂t A. We'll approximate ∂t A by difference if previous A is stored externally.
    # Here, we assume ∂t A ~ 0 (or user can supply a previous A_vec to compute derivative).
    E_vec = - np.gradient(Phi_val)[0] * np.ones_like(grad_Xi_vals)  # (placeholder gradient of scalar)
    # Actually, to get E properly: E = -grad(Phi) - dA/dt. We can compute -grad(Phi) easily:
    grad_Phi = np.zeros_like(grad_Xi_vals)
    for i in range(grad_Phi.shape[1]):
        grad_Phi[:, i] = fem.assemble_scalar(fem.form(fem.derivative(Xi * 0 + Chi * 0 + Phi_val, Xi)))  # (pseudo-code)
    # (In practice, computing grad_Phi and dA/dt in FEniCSx needs proper variational or difference approach)

    # Compute B = curl(A). In 3D, B has 3 components. We can use FEniCSx’s curl operator if available, or manual.
    # For simplicity, pseudo-code using numpy for curl on structured data or ignore if 2D.
    B_vec = np.zeros_like(grad_Xi_vals)
    # ... compute curl of A_vec

    # Effective charge density: rho_eff = ∇·E (we can approximate via divergence of E_vec)
    rho_eff = np.zeros(len(Xi.x.array))
    # ... compute divergence of E_vec

    # Effective current: J_eff = curl(B) - dE/dt (not computed in detail here)

    return {"E": E_vec, "B": B_vec, "rho_eff": rho_eff, "A": A_vec, "Phi": Phi_val}

