
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import laplace

# Grid and time parameters
nx, ny, nz = 64, 64, 64
dx = dy = dz = 0.1
dt = 0.01
steps = 1000  # For demonstration; extend as needed

# Physical parameters
D_xi = 0.05
D_chi = 0.1
alpha_0 = 0.1
gamma = 0.2
beta = 1.0

# Initial fields
X = np.linspace(-3, 3, nx)
Y = np.linspace(-3, 3, ny)
Z = np.linspace(-3, 3, nz)
Xg, Yg, Zg = np.meshgrid(X, Y, Z, indexing='ij')

Xi = np.exp(-0.5 * (Xg**2 + Yg**2 + Zg**2))
chi = np.random.normal(0, 0.05, size=(nx, ny, nz))

# Toroidal coherence seed
R = 1.0
r = 0.3
toroid = lambda x, y, z: (np.sqrt(x**2 + y**2) - R)**2 + z**2 - r**2
chi += np.exp(-toroid(Xg, Yg, Zg)**2 / 0.05)

# Time-varying alpha(t)
def alpha(t): return alpha_0 * np.tanh(t / 200)

# Stochastic noise generator
def eta(shape, scale=0.01): return np.random.normal(0, scale, size=shape)

# Time evolution
for step in range(steps):
    lap_xi = laplace(Xi, mode='reflect') / dx**2
    lap_chi = laplace(chi, mode='reflect') / dx**2

    grad_chi_x, grad_chi_y, grad_chi_z = np.gradient(chi, dx, dy, dz)
    grad_chi_sq = grad_chi_x**2 + grad_chi_y**2 + grad_chi_z**2

    a_t = alpha(step)
    dXi_dt = D_xi * lap_xi + a_t * grad_chi_sq - beta * Xi**2 + eta(Xi.shape)
    dchi_dt = D_chi * lap_chi - gamma * Xi * chi + eta(chi.shape)

    Xi += dt * dXi_dt
    chi += dt * dchi_dt

# Save final slices for inspection
np.savez("XiChi3D_result.npz", Xi=Xi[nx//2], chi=chi[nx//2])
