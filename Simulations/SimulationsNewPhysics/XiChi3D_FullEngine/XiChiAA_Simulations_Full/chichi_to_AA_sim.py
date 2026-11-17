
import numpy as np
import matplotlib.pyplot as plt

# Physical constants
g_chiAA = 0.08
mass_chi = 0.5
mass_A = 0.0
nx = 200
dx = 0.1
timesteps = 500
dt = 0.01

# Initial chi field with toroidal-like bump and empty Aμ
x = np.linspace(-10, 10, nx)
chi = np.exp(-((x - 3)**2)) - np.exp(-((x + 3)**2))
A = np.zeros(nx)

# Propagation
def propagate_field(field, mass, dx, dt):
    lap = np.roll(field, 1) + np.roll(field, -1) - 2 * field
    return field + dt * (lap / dx**2 - mass**2 * field)

def interact(chi, A, g):
    return g * chi**2

A_history = []

for t in range(timesteps):
    chi = propagate_field(chi, mass_chi, dx, dt)
    A += dt * (propagate_field(A, mass_A, dx, dt) + interact(chi, A, g_chiAA))
    A_history.append(np.copy(A))

plt.plot(x, A, label="Aμ from χχ scattering")
plt.title("χχ → AA field generation")
plt.xlabel("x")
plt.ylabel("Field strength")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("chichi_to_AA_output.png")
