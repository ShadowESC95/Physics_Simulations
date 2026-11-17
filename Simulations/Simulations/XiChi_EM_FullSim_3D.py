
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import laplace

# Simulation grid parameters
nx, ny, nz = 64, 64, 64
dx = dy = dz = 0.2
dt = 0.01
steps = 500

# Physical constants and coupling parameters
D_xi = 0.1       # Diffusivity of Ξ field
D_chi = 0.05     # Diffusivity of χ field
D_A = 0.2        # EM field diffusivity
alpha = 1.0      # Coherence coupling
beta = 1.0       # Saturation
gamma = 0.5      # Damping
g_em = 0.3       # EM coupling strength
lambda_phi = 0.8 # Self-interaction strength

# Fields
Xi = np.random.rand(nx, ny, nz)
chi = np.random.rand(nx, ny, nz)
A = np.zeros((nx, ny, nz))

# Initial EM seeding in center
cx, cy, cz = nx//2, ny//2, nz//2
A[cx-1:cx+2, cy-1:cy+2, cz-1:cz+2] = 1.0

def compute_laplacian(f):
    return (np.roll(f, 1, axis=0) + np.roll(f, -1, axis=0) +
            np.roll(f, 1, axis=1) + np.roll(f, -1, axis=1) +
            np.roll(f, 1, axis=2) + np.roll(f, -1, axis=2) - 6 * f) / dx**2

# Time evolution
for step in range(steps):
    lap_Xi = compute_laplacian(Xi)
    lap_chi = compute_laplacian(chi)
    lap_A = compute_laplacian(A)

    grad_chi_x = (np.roll(chi, -1, axis=0) - np.roll(chi, 1, axis=0)) / (2 * dx)
    grad_chi_y = (np.roll(chi, -1, axis=1) - np.roll(chi, 1, axis=1)) / (2 * dy)
    grad_chi_z = (np.roll(chi, -1, axis=2) - np.roll(chi, 1, axis=2)) / (2 * dz)
    grad_chi_sq = grad_chi_x**2 + grad_chi_y**2 + grad_chi_z**2

    # Reaction terms
    dXi_dt = D_xi * lap_Xi + alpha * grad_chi_sq - beta * Xi**2
    dchi_dt = D_chi * lap_chi - gamma * Xi * chi
    dA_dt = D_A * lap_A + g_em * chi**2 - lambda_phi * A**3

    Xi += dt * dXi_dt
    chi += dt * dchi_dt
    A += dt * dA_dt

# Save final slices
np.save("final_Xi_slice.npy", Xi[:, :, nz//2])
np.save("final_chi_slice.npy", chi[:, :, nz//2])
np.save("final_A_slice.npy", A[:, :, nz//2])
