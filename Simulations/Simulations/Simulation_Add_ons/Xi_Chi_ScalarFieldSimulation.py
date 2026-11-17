
import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
nx, ny = 2000, 2000
dx = dy = 0.1
dt = 0.001
nt = 5000

lambda_ = 1.0
Gamma = 1.2
delta = 0.1

# Initialize fields
Xi = np.zeros((nx, ny))
Chi = np.zeros((nx, ny))
Xi_new = np.zeros_like(Xi)
Chi_new = np.zeros_like(Chi)
Xi_old = np.zeros_like(Xi)
Chi_old = np.zeros_like(Chi)

# Initial Gaussian blobs
x = np.linspace(-10, 10, nx)
y = np.linspace(-10, 10, ny)
X, Y = np.meshgrid(x, y, indexing='ij')
r2 = X**2 + Y**2
Xi[:] = np.exp(-r2 / 2)
Chi[:] = 0.5 * np.exp(-r2 / 4)
Xi_old[:] = Xi[:]
Chi_old[:] = Chi[:]

def laplacian(field):
    return (
        -4 * field
        + np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1)
    ) / dx**2

def dV_dXi(Xi, Chi):
    return 4 * lambda_ * (Xi * Chi - Gamma) * Chi * ((Xi * Chi - Gamma)**2 + delta**2)

def dV_dChi(Xi, Chi):
    return 4 * lambda_ * (Xi * Chi - Gamma) * Xi * ((Xi * Chi - Gamma)**2 + delta**2)

save_interval = 1000
output_dir = "xi_chi_output"
os.makedirs(output_dir, exist_ok=True)

for t in range(nt):
    lap_Xi = laplacian(Xi)
    lap_Chi = laplacian(Chi)

    Xi_new = 2 * Xi - Xi_old + dt**2 * (lap_Xi - dV_dXi(Xi, Chi))
    Chi_new = 2 * Chi - Chi_old + dt**2 * (lap_Chi - dV_dChi(Xi, Chi))

    Xi_old[:], Xi[:] = Xi[:], Xi_new[:]
    Chi_old[:], Chi[:] = Chi[:], Chi_new[:]

    if t % save_interval == 0:
        np.savez_compressed(os.path.join(output_dir, f"fields_t{t:04d}.npz"), Xi=Xi, Chi=Chi)
        print(f"Saved frame at t = {t}")

print("Simulation complete.")
