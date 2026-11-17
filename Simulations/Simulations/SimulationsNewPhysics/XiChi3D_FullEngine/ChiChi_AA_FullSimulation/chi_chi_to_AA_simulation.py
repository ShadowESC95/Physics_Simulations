# χχ → AA Simulation Script
# Full logic with electromagnetic tensor, nuclear forces, and curvature feedback

import numpy as np
from scipy.ndimage import laplace
import matplotlib.pyplot as plt

# Grid setup
nx, ny = 128, 128
dx = dy = 0.05
dt = 0.001
steps = 10000

# Parameters (including electromagnetic, nuclear, entropy-coherence coupling)
alpha_t = lambda t: 1 + 0.5 * np.sin(0.01 * t)
gamma = 0.2
beta = 1.0
delta = 0.05
E_strength = 0.3
B_strength = 0.2
strong_force_coupling = 0.8
weak_force_coupling = 0.1

# Initialize fields
X = np.linspace(-3, 3, nx)
Y = np.linspace(-3, 3, ny)
Xg, Yg = np.meshgrid(X, Y)
chi1 = np.exp(-0.5 * (Xg**2 + Yg**2))
chi2 = 0.1 * np.random.randn(nx, ny)
A_field = np.zeros((nx, ny))

# Time evolution
for step in range(steps):
    t = step * dt
    a_t = alpha_t(t)

    lap_chi1 = laplace(chi1, mode="reflect") / dx**2
    lap_chi2 = laplace(chi2, mode="reflect") / dx**2

    grad_chi1_x, grad_chi1_y = np.gradient(chi1, dx, dy)
    grad_chi2_x, grad_chi2_y = np.gradient(chi2, dx, dy)

    entropy_input = grad_chi1_x**2 + grad_chi2_y**2
    curvature_term = 0.02 * (Xg**2 - Yg**2)

    # EM & nuclear feedbacks
    A_feedback = E_strength * chi1 - B_strength * chi2
    nuclear_feedback = strong_force_coupling * chi1 * chi2 - weak_force_coupling * lap_chi2

    # Dynamics
    dchi1_dt = delta * lap_chi1 + a_t * entropy_input - gamma * chi1**3 + curvature_term + nuclear_feedback
    dchi2_dt = delta * lap_chi2 - beta * chi2**3 + A_feedback

    chi1 += dt * dchi1_dt
    chi2 += dt * dchi2_dt
    A_field += dt * (chi1 * chi2 - A_field)

# Plot output
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(chi1, cmap="inferno", origin="lower")
axes[0].set_title("χ₁ field")
axes[1].imshow(chi2, cmap="viridis", origin="lower")
axes[1].set_title("χ₂ field")
axes[2].imshow(A_field, cmap="plasma", origin="lower")
axes[2].set_title("Emergent A Field")
plt.tight_layout()
plt.show()
