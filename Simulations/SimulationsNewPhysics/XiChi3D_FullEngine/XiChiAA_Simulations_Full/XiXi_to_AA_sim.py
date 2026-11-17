
import numpy as np
import matplotlib.pyplot as plt

# Physical constants (symbolic placeholder values)
g_XiAA = 0.1  # coupling constant ΞΞAμAμ
mass_Xi = 1.0
mass_A = 0.0
volume = 100.0
timesteps = 500

# Initial field amplitudes Ξ and Aμ (simplified 1D lattice for simulation)
nx = 200
dx = 0.1
Xi = np.exp(-((np.linspace(-10, 10, nx))**2)) * 0.5
A = np.zeros(nx)

# Propagators: scalar Ξ and massless gauge field Aμ
def propagate_field(field, mass, dx, dt):
    lap = np.roll(field, 1) + np.roll(field, -1) - 2 * field
    return field + dt * (lap / dx**2 - mass**2 * field)

# Interaction: ΞΞ → AA via g_XiAA Ξ^2 Aμ^2 term (simplified)
def interact(Xi, A, g):
    return g * Xi**2

dt = 0.01
A_history = []

for t in range(timesteps):
    Xi = propagate_field(Xi, mass_Xi, dx, dt)
    interaction = interact(Xi, A, g_XiAA)
    A += dt * (propagate_field(A, mass_A, dx, dt) + interaction)
    A_history.append(np.copy(A))

# Plot final field A
plt.plot(np.linspace(-10, 10, nx), A, label="Aμ at final timestep")
plt.title("ΞΞ → AA scattering (simplified)")
plt.xlabel("x")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("XiXi_to_AA_output.png")
