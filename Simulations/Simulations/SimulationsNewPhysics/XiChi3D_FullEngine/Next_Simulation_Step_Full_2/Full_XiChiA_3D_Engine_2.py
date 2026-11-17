import numpy as np
import h5py
from scipy.ndimage import laplace
import os

# Grid parameters
nx, ny, nz = 64, 64, 64
dx = dy = dz = 0.1
dt = 0.01
steps = 1000  # You can increase this to 10000 or more as needed

# Physical parameters from your framework
D_xi = 0.1
alpha0 = 1.0
gamma = 1.0
beta = 1.0
delta = 0.1
eta_strength = 0.05
epsilon_0 = 8.854e-12
mu_0 = 1.257e-6

# Initialize fields
Xi = np.exp(-((np.indices((nx, ny, nz))[0] - nx//2)**2 +
              (np.indices((nx, ny, nz))[1] - ny//2)**2 +
              (np.indices((nx, ny, nz))[2] - nz//2)**2) / 50.0)

chi = 0.05 * np.random.randn(nx, ny, nz)
A = 0.01 * np.random.randn(nx, ny, nz)

# Utility functions
def lap3d(field):
    return laplace(field, mode='reflect') / dx**2

def save_to_hdf5(step, Xi, chi, A):
    with h5py.File(f"{step:06d}.h5", "w") as f:
        f.create_dataset("Xi", data=Xi)
        f.create_dataset("chi", data=chi)
        f.create_dataset("A", data=A)

# Time evolution
for step in range(steps):
    alpha = alpha0 * (step / steps)  # time-varying coherence forcing
    eta = eta_strength * np.random.randn(nx, ny, nz)

    lap_Xi = lap3d(Xi)
    lap_chi = lap3d(chi)
    lap_A = lap3d(A)

    grad_chi_x = np.gradient(chi, dx, axis=0)
    grad_chi_y = np.gradient(chi, dy, axis=1)
    grad_chi_z = np.gradient(chi, dz, axis=2)
    grad_chi_sq = grad_chi_x**2 + grad_chi_y**2 + grad_chi_z**2

    dXi_dt = D_xi * lap_Xi + alpha * grad_chi_sq - beta * Xi**2 + eta
    dchi_dt = -gamma * Xi * chi + delta * lap_chi
    dA_dt = (1 / epsilon_0) * (lap_A + gamma * Xi - beta * chi * A)

    Xi += dt * dXi_dt
    chi += dt * dchi_dt
    A += dt * dA_dt

    if step % 100 == 0:
        save_to_hdf5(step, Xi, chi, A)
