import numpy as np
import matplotlib.pyplot as plt

# Constants (in natural units where hbar = c = k_B = 1)
G_0 = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
c_0 = 3.0e8  # Speed of light (m/s)
hbar = 1.05457e-34  # Reduced Planck’s constant (J·s)
k_B = 1.38065e-23  # Boltzmann constant (J/K)
M_sun = 1.989e30  # Solar mass (kg)
A_BH = 4 * np.pi * (2 * G_0 * M_sun / c_0**2)**2  # Black hole area for 1 solar mass
f_P = c_0**5 / (G_0 * hbar)  # Planck frequency

# Adjustable parameters for frequency-dependent G and c
alpha = 0.1  # Scaling parameter for G variation
beta = 0.1  # Scaling parameter for c variation

# Frequency range (logarithmic scale)
f_range = np.logspace(np.log10(f_P / 1e10), np.log10(f_P), 100)

# Compute entropy and temperature modifications
def entropy(f):
    G_f = G_0 * (1 + alpha * np.log(f / f_P))  # Variable G
    c_f = c_0 * (1 + beta * np.log(f / f_P))**-1  # Variable c
    return (k_B * A_BH / (4 * hbar)) * (c_f**3 / G_f)

def temperature(f):
    G_f = G_0 * (1 + alpha * np.log(f / f_P))  # Variable G
    c_f = c_0 * (1 + beta * np.log(f / f_P))**-1  # Variable c
    return (hbar * c_f**3) / (8 * np.pi * G_f * k_B * M_sun)

S_values = entropy(f_range)
T_values = temperature(f_range)

# Plot entropy and temperature vs. frequency
fig, axs = plt.subplots(2, 1, figsize=(8, 10))

axs[0].plot(f_range / f_P, S_values, label="Entropy S_BH(f)", color='blue')
axs[0].set_xscale("log")
axs[0].set_yscale("log")
axs[0].set_xlabel("f / f_P (normalized frequency)")
axs[0].set_ylabel("Entropy S_BH")
axs[0].legend()
axs[0].grid(True)

axs[1].plot(f_range / f_P, T_values, label="Temperature T(f)", color='red')
axs[1].set_xscale("log")
axs[1].set_yscale("log")
axs[1].set_xlabel("f / f_P (normalized frequency)")
axs[1].set_ylabel("Temperature T_BH")
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
