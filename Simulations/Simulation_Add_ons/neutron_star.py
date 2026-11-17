import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---- Generate or load G(Ξ) values from the 200-step Model 2 run ----
# For demonstration, we create a small drift over time; replace this with your simulation data
G_steps = 1000
np.random.seed(0)
G_vals = 6.67430e-11 * (1 + 0.03 * np.sin(np.linspace(0, 4*np.pi, G_steps)))  # Example: ~3% modulation

# ---- Simulate orbital decay ----
P_dot_GR = 1.0  # Normalized GR prediction
P_dot_Xi = (G_vals / G_vals[0]) ** (5/3)  # Quadrupole scaling

df_decay = pd.DataFrame({
    "step": np.arange(len(G_vals)),
    "G_Xi": G_vals,
    "P_dot_Xi": P_dot_Xi
})
df_decay.to_csv("NeutronStar_OrbitalDecay_GXi.csv", index=False)

# ---- Plot orbital decay ratio vs GR ----
plt.figure(figsize=(8, 5))
plt.plot(df_decay["step"], df_decay["P_dot_Xi"], label=r"$\dot{P}_\mathrm{model} / \dot{P}_\mathrm{GR}$")
plt.axhline(1.0, color='gray', linestyle='--', label="GR Baseline")
plt.title("Neutron Star Orbital Decay from G(Ξ)")
plt.xlabel("Time Step")
plt.ylabel("Relative Orbital Decay Rate")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("NeutronStar_OrbitalDecay_GXi.png")
plt.close()

print("Saved decay data: NeutronStar_OrbitalDecay_GXi.csv")
print("Saved plot: NeutronStar_OrbitalDecay_GXi.png")

