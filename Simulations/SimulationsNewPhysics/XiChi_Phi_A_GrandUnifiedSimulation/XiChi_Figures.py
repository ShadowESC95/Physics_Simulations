import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import laplace

# Simulation parameters
nx, ny = 100, 100
dx = dy = 0.1
dt = 0.01
steps = 1000

# PDE parameters
D_xi = 0.1     # diffusion coefficient for Xi
alpha = 1.0    # coherence gradient to entropy coupling
beta = 1.0     # saturation term for Xi
gamma = 1.0    # coherence decay coupling
delta = 0.1    # diffusion coefficient for chi

# Initialize fields Xi and chi
X = np.linspace(-5, 5, nx)
Y = np.linspace(-5, 5, ny)
Xg, Yg = np.meshgrid(X, Y)

# Initial conditions: Xi gaussian, chi random small fluctuations
Xi = np.exp(-0.5*(Xg**2+Yg**2))
chi = 0.1 * np.random.randn(nx, ny)

# Time evolution
for step in range(steps):
    # Compute Laplacians
    lap_xi = laplace(Xi, mode='reflect') / dx**2
    lap_chi = laplace(chi, mode='reflect') / dx**2
    
    # Compute non-linear terms
    grad_chi_x, grad_chi_y = np.gradient(chi, dx, dy)
    grad_chi_sq = grad_chi_x**2 + grad_chi_y**2
    
    # Update rules
    dXi_dt = D_xi * lap_xi + alpha * grad_chi_sq - beta * Xi**2
    dchi_dt = -gamma * Xi * chi + delta * lap_chi
    
    Xi += dt * dXi_dt
    chi += dt * dchi_dt

# Plot final fields
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(Xi, extent=[-5,5,-5,5], origin='lower', cmap='inferno')
axes[0].set_title(r'$\Xi(x,y)$ at final time')
plt.colorbar(im0, ax=axes[0])
im1 = axes[1].imshow(chi, extent=[-5,5,-5,5], origin='lower', cmap='viridis')
axes[1].set_title(r'$\chi(x,y)$ at final time')
plt.colorbar(im1, ax=axes[1])
plt.tight_layout()
plt.show()
