
import numpy as np
import matplotlib.pyplot as plt

# Grid parameters
dx = 1e-9  # 1 nm
dt = dx / (2.998e8 * np.sqrt(2))  # Courant condition
L = 2000  # number of grid points
T = 1200  # number of time steps

# Fields
Ez = np.zeros(L)
Hy = np.zeros(L)

# Permittivity profile (DBR)
eps_r = np.ones(L)
n1, n2 = 1.45, 2.1
d1, d2 = 100, 100  # in grid points
for i in range(10):
    eps_r[i*(d1+d2):i*(d1+d2)+d1] = n1**2
    eps_r[i*(d1+d2)+d1:i*(d1+d2)+d1+d2] = n2**2

# Main loop
Ez_data = []
for t in range(T):
    Hy[:-1] += (Ez[1:] - Ez[:-1]) * dt / (dx * 4e-7 * np.pi)
    Ez[1:] += (Hy[1:] - Hy[:-1]) * dt / (dx * 8.85e-12 * eps_r[1:])
    Ez[50] += np.exp(-0.5 * ((t - 100)/20)**2)  # Source

    if t % 10 == 0:
        Ez_data.append(Ez.copy())

# Plot final snapshot
plt.imshow(np.array(Ez_data).T, aspect='auto', cmap='seismic', extent=[0, T*dt*1e15, 0, L*dx*1e9])
plt.xlabel("Time (fs)")
plt.ylabel("Position (nm)")
plt.title("Ez Field Propagation through DBR (Yee Grid)")
plt.colorbar(label="Ez")
plt.tight_layout()
plt.show()
