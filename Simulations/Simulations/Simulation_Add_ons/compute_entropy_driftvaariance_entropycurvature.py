import matplotlib.pyplot as plt
import numpy as np

# ---- Simulate a toy trajectory of scalar field Ξ ----
# Example: oscillating + diffusive random field
N_steps = 200
field_shape = (32, 32)  # adjust as desired (spatial size)

xi_traj = []
xi = np.random.randn(*field_shape) * 0.1   # initial condition

for t in range(N_steps):
    # Random walk + sinusoidal modulation as a toy model
    noise = np.random.randn(*field_shape) * 0.02
    xi = xi + noise + 0.04 * np.sin(2 * np.pi * t / 40)  # slow oscillation
    xi_traj.append(np.copy(xi))

xi_traj = np.array(xi_traj)  # Shape: (N_steps, y, x)

# ---- Compute entropy S(t), drift variance V_D(t), and entropy curvature C(t) ----
def compute_entropy_and_variance(xi_traj):
    S_list = []
    VD_list = []
    for xi in xi_traj:
        xi_abs = np.abs(xi)
        p = xi_abs / np.sum(xi_abs)
        p = p[p > 0]
        S = -np.sum(p * np.log(p))
        S_list.append(S)

        grad_y, grad_x = np.gradient(xi)
        grad_mag_sq = grad_x**2 + grad_y**2
        VD = np.var(grad_mag_sq)
        VD_list.append(VD)

    S_array = np.array(S_list)
    C_array = np.gradient(np.gradient(S_array))
    return S_array, VD_list, C_array

S_vals, VD_vals, C_vals = compute_entropy_and_variance(xi_traj)

# ---- Plot results ----
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

axs[0].plot(S_vals, label="Entropy S(t)")
axs[0].set_ylabel("S(t)")
axs[0].legend()

axs[1].plot(VD_vals, label="Drift Variance V_D(t)", color='orange')
axs[1].set_ylabel("V_D(t)")
axs[1].legend()

axs[2].plot(C_vals, label="Entropy Curvature C(t)", color='green')
axs[2].axhline(0, color='gray', linestyle='--')
axs[2].set_xlabel("Time Step")
axs[2].set_ylabel("C(t)")
axs[2].legend()

plt.tight_layout()
plt.savefig("entropy_drift_variance_curvature.png")
plt.show()

print("Saved figure as entropy_drift_variance_curvature.png")

