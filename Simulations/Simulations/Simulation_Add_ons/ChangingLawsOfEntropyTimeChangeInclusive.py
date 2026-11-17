import numpy as np
import matplotlib.pyplot as plt

# Constants (you need to define these based on your context)
G_0 = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
c_0 = 3.00e8  # Speed of light in m/s
M_sun = 1.989e30  # Mass of the sun in kg
alpha = 0.1  # Example value for alpha
beta = 0.1  # Example value for beta
f_P = 1.0  # Example value for Planck frequency
f_range = np.logspace(1, 10, 100)  # Example frequency range
S_values = np.random.rand(100)  # Example entropy values
T_values = np.random.rand(100)  # Example temperature values

# Compute time dilation as a function of frequency
def time_dilation(f, r):
    G_f = G_0 * (1 + alpha * np.log(f / f_P))  # Variable G
    c_f = c_0 * (1 + beta * np.log(f / f_P))**-1  # Variable c
    rs = 2 * G_f * M_sun / c_f**2  # Schwarzschild radius with variable G, c
    # Ensure rs / r is less than 1 to avoid invalid sqrt operation
    rs_r_ratio = rs / r
    rs_r_ratio = np.clip(rs_r_ratio, 0, 0.9999999999999999)
    return np.sqrt(1 - rs_r_ratio)

# Define observation radii (near event horizon and further out)
r_horizon = 2 * G_0 * M_sun / c_0**2  # Standard Schwarzschild radius
r_outer = 10 * r_horizon  # Arbitrary distance further from BH

# Compute time dilation near horizon and further out
td_horizon = time_dilation(f_range, r_horizon)
td_outer = time_dilation(f_range, r_outer)

# Updated Entropy & Temperature Adjusted for Time Dilation
S_values_dilated = S_values * td_horizon  # Scale entropy by time dilation
T_values_dilated = T_values / td_horizon  # Inverse effect on temperature

# Debug prints to check initial arrays
print("Initial f_range:", f_range)
print("Initial S_values_dilated:", S_values_dilated)
print("Initial T_values_dilated:", T_values_dilated)

# Filter out non-positive values for log scaling
positive_indices = (f_range > 0) & (S_values_dilated > 0) & (T_values_dilated > 0)
f_range = f_range[positive_indices]
td_horizon = td_horizon[positive_indices]
td_outer = td_outer[positive_indices]
S_values_dilated = S_values_dilated[positive_indices]
T_values_dilated = T_values_dilated[positive_indices]

# Debug prints to check filtered arrays
print("Filtered f_range:", f_range)
print("Filtered S_values_dilated:", S_values_dilated)
print("Filtered T_values_dilated:", T_values_dilated)

# Check if there are any positive values left after filtering
if len(f_range) == 0 or len(S_values_dilated) == 0 or len(T_values_dilated) == 0:
    raise ValueError("Filtered data has no positive values for log scaling.")

# Plot results
fig, axs = plt.subplots(3, 1, figsize=(8, 12))

axs[0].plot(f_range / f_P, td_horizon, label="Time Dilation at Event Horizon", color='green')
axs[0].plot(f_range / f_P, td_outer, label="Time Dilation Further Out", color='purple', linestyle='dashed')
axs[0].set_xscale("log")
axs[0].set_xlabel("f / f_P (normalized frequency)")
axs[0].set_ylabel("Time Dilation Factor")
axs[0].legend()
axs[0].grid(True)

axs[1].plot(f_range / f_P, S_values_dilated, label="Entropy Adjusted for Time Dilation", color='blue')
axs[1].set_xscale("log")
axs[1].set_yscale("log")
axs[1].set_xlabel("f / f_P (normalized frequency)")
axs[1].set_ylabel("Entropy S_BH (dilated)")
axs[1].legend()
axs[1].grid(True)

axs[2].plot(f_range / f_P, T_values_dilated, label="Temperature Adjusted for Time Dilation", color='red')
axs[2].set_xscale("log")
axs[2].set_yscale("log")
axs[2].set_xlabel("f / f_P (normalized frequency)")
axs[2].set_ylabel("Temperature T_BH (dilated)")
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()