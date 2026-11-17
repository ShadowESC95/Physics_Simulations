
import numpy as np
import h5py
import matplotlib.pyplot as plt

# Constants from the full Lagrangian
D_xi = 0.05          # diffusion coefficient for Xi
alpha_t = lambda t: 0.1 + 0.05 * np.tanh(t / 500)  # time-varying coherence coupling
beta = 0.01          # nonlinear saturation
gamma = 0.1          # coupling to chi
delta = 0.04         # diffusion for chi
e_charge = 1.0       # electric charge
g_weak = 0.65        # weak coupling constant
g_strong = 1.2       # strong coupling constant
curv_term = 0.001    # small spacetime curvature correction

# Simulation grid
nx, ny = 128, 128
dx = dy = 0.1
dt = 0.01
steps = 2000

# Initialize fields
Xi = np.exp(-((np.linspace(-6, 6, nx)[:, None])**2 + (np.linspace(-6, 6, ny)[None, :])**2)/4)
chi = 0.01 * np.random.randn(nx, ny)
A_field = np.zeros((nx, ny))  # electromagnetic potential field

# Time evolution
for t in range(steps):
    lap_Xi = (np.roll(Xi, 1, axis=0) + np.roll(Xi, -1, axis=0) +
              np.roll(Xi, 1, axis=1) + np.roll(Xi, -1, axis=1) - 4 * Xi) / dx**2

    lap_chi = (np.roll(chi, 1, axis=0) + np.roll(chi, -1, axis=0) +
               np.roll(chi, 1, axis=1) + np.roll(chi, -1, axis=1) - 4 * chi) / dx**2

    grad_chi_x, grad_chi_y = np.gradient(chi, dx, dy)
    grad_chi_sq = grad_chi_x**2 + grad_chi_y**2

    # Field equations including curvature and EM feedback
    dXi_dt = D_xi * lap_Xi + alpha_t(t) * grad_chi_sq - beta * Xi**3 + curv_term * Xi
    dchi_dt = -gamma * Xi * chi + delta * lap_chi + e_charge**2 * A_field * chi

    # Update EM potential A (simplified)
    dA_dt = g_weak * Xi * chi - g_strong * A_field**2 + 0.05 * np.random.randn(nx, ny)

    # Time step updates
    Xi += dt * dXi_dt
    chi += dt * dchi_dt
    A_field += dt * dA_dt

# Save final fields
with h5py.File('XiChiAA_FinalState.h5', 'w') as f:
    f.create_dataset("Xi", data=Xi)
    f.create_dataset("chi", data=chi)
    f.create_dataset("A_field", data=A_field)

# Plotting output for verification
fig, axs = plt.subplots(1, 3, figsize=(12, 4))
axs[0].imshow(Xi, cmap='inferno', origin='lower'); axs[0].set_title("Ξ field")
axs[1].imshow(chi, cmap='viridis', origin='lower'); axs[1].set_title("χ field")
axs[2].imshow(A_field, cmap='plasma', origin='lower'); axs[2].set_title("Aμ field")
plt.tight_layout(); plt.savefig("XiChiAA_Output.png")
