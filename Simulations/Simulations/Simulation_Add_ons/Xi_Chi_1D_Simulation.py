
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
L = 10.0             # Length of spatial domain
T = 5.0              # Total simulation time
Nx = 200             # Number of spatial points
Nt = 1000            # Number of time steps
dx = L / Nx
dt = T / Nt
x = np.linspace(0, L, Nx)
c = 1.0              # Wave speed

# Initialize fields
Xi = np.exp(-((x - L/2)**2))     # Gaussian initial Ξ
chi = np.zeros(Nx)              # Zero initial χ
Xi_new = np.copy(Xi)
Xi_old = np.copy(Xi)
chi_new = np.copy(chi)
chi_old = np.copy(chi)

# Simple potential (stabilizer): V(Xi, chi) = lambda * Xi^2 * chi^2
lambda_int = 0.1

# Storage for entropy flux divergence
entropy_div = []

# Simulation loop
for n in range(Nt):
    # Compute Laplacian
    Xi_xx = (np.roll(Xi, -1) - 2*Xi + np.roll(Xi, 1)) / dx**2
    chi_xx = (np.roll(chi, -1) - 2*chi + np.roll(chi, 1)) / dx**2

    # Update using simple finite difference wave equation with potential
    Xi_new = 2*Xi - Xi_old + (dt**2) * (c**2 * Xi_xx - lambda_int * (chi**2) * Xi)
    chi_new = 2*chi - chi_old + (dt**2) * (c**2 * chi_xx - lambda_int * (Xi**2) * chi)

    # Entropy divergence approx: ∂t Xi (simple version)
    entropy_div.append(np.mean((Xi - Xi_old) / dt))

    # Step forward
    Xi_old, Xi = Xi, Xi_new
    chi_old, chi = chi, chi_new

# Plot final fields and entropy divergence
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(x, Xi, label='Ξ(x,T)')
plt.plot(x, chi, label='χ(x,T)')
plt.title("Final Fields at t = T")
plt.xlabel("x")
plt.ylabel("Field Value")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(np.linspace(0, T, Nt), entropy_div)
plt.title("Mean Entropy Flux Divergence")
plt.xlabel("Time")
plt.ylabel("∇·Sμ (approx)")

plt.tight_layout()
plt.savefig("Xi_Chi_1D_Simulation.png")
plt.show()
