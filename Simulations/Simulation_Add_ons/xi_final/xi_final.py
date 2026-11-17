import numpy as np
import matplotlib.pyplot as plt

# ---- Generate synthetic final field snapshot ----
np.random.seed(0)
xi_final = np.random.randn(32, 32) * 0.1   # Replace with your simulation if needed

# ---- Rest of your script ----
xi_entropy = xi_final.copy()

# Compute entropy flow J_S = Ξ ∇Ξ, then divergence ∇ · J_S
grad_y, grad_x = np.gradient(xi_entropy)
Jx = xi_entropy * grad_x
Jy = xi_entropy * grad_y
div_Js = np.gradient(Jx, axis=1) + np.gradient(Jy, axis=0)

entropy_flux_mean = np.mean(div_Js)
entropy_flux_std = np.std(div_Js)

# Export data
entropy_flux_map = div_Js
np.save("EntropyFlux_DivergenceJS.npy", entropy_flux_map)  # to current working dir

# Plot entropy source/sink map
plt.figure(figsize=(7, 6))
plt.imshow(entropy_flux_map, cmap='seismic', origin='lower')
plt.colorbar(label=r"$\nabla \cdot \vec{J}_S$")
plt.title("Entropy Flux Divergence (Curvature Detector)")
plt.tight_layout()

plt.savefig("EntropyFlux_DivergenceJS.png")
plt.close()

print("Saved image as EntropyFlux_DivergenceJS.png")

