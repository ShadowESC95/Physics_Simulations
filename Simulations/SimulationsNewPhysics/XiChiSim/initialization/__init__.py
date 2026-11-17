# initialization/field_init.py
import numpy as np
from dolfinx import fem

def initialize_fields(Xi_function: fem.Function, Chi_function: fem.Function, profile="quiescent"):
    """
    Initialize the Ξ and χ fields on the given FEniCSx Function objects.
    Available profiles: "quiescent", "random", "point_charge", "vortex", etc.
    """
    mesh = Xi_function.function_space.mesh
    coords = mesh.geometry.x  # coordinates of mesh points

    if profile == "quiescent":
        # Zero fields everywhere
        Xi_function.x.array[:] = 0.0
        Chi_function.x.array[:] = 0.0

    elif profile == "random":
        # Small random noise in both fields
        np.random.seed(42)
        Xi_function.x.array[:] = 1e-6 * (np.random.rand(len(Xi_function.x.array)) - 0.5)
        Chi_function.x.array[:] = 1e-6 * (np.random.rand(len(Chi_function.x.array)) - 0.5)

    elif profile == "point_charge":
        # Ξ as 1/r potential around center, χ = 0. (Assumes a point charge at domain center)
        L = np.max(coords, axis=0) - np.min(coords, axis=0)  # domain side lengths
        center = np.min(coords, axis=0) + L/2
        eps = 0.02 * np.linalg.norm(L)  # small regularization to avoid singularity
        Xi_vals = []
        for pt in coords:
            r = np.linalg.norm(pt - center)
            # Coulomb potential: Ξ ~ (1/(4πε0)) * (q/r). For unit q in normalized units:
            phi = 1.0 / (4 * np.pi * ε0 * (r + eps))
            Xi_vals.append(gamma * phi)  # include gamma factor if needed
        Xi_function.x.array[:] = np.array(Xi_vals)
        Chi_function.x.array[:] = 0.0

    elif profile == "vortex":
        # Topological defect in χ: e.g., χ varies from 0 to 2π around z-axis (a simple vortex line)
        Chi_vals = []
        for pt in coords:
            x, y, z = pt
            angle = np.arctan2(y - 0.5, x - 0.5)  # angle around center of domain
            Chi_vals.append(angle)  # assign χ = angle (in radians)
        Chi_function.x.array[:] = np.array(Chi_vals)
        # Ξ maybe zero or a small perturbation
        Xi_function.x.array[:] = 0.0

    else:
        raise ValueError(f"Unknown profile: {profile}")

