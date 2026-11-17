import numpy as np
import matplotlib.pyplot as plt

# Constants
k_B = 1.380649e-23  # Boltzmann constant (J/K)
m_consciousness = 1e-5  # Assumed mass for consciousness in kg (arbitrary for this simulation)
f_max = 900  # Maximum frequency (Hz)
S0 = 1  # Base entropy (arbitrary units)
t_0 = 1  # Base time (arbitrary time unit)

# Frequency range from 0 Hz to 900 Hz
frequencies = np.linspace(0.1, f_max, 900)  # Avoid zero to prevent log(0)

# Entropy S(f) = S0 + k_B * log(f)
entropy = S0 + k_B * np.log(frequencies)

# Energy E(f) = 1/2 * m_consciousness * f^2
energy = 0.5 * m_consciousness * frequencies**2

# Time dilation t(f) = t_0 * (1 + f/f_max)
time_dilation = t_0 * (1 + frequencies / f_max)

# Plot Entropy vs Frequency
plt.figure(figsize=(14, 5))

plt.subplot(1, 3, 1)
plt.plot(frequencies, entropy, label="Entropy (S)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Entropy (S)")
plt.title("Entropy vs Frequency")
plt.grid(True)

# Plot Energy vs Frequency
plt.subplot(1, 3, 2)
plt.plot(frequencies, energy, label="Energy (E)", color='orange')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Energy (J)")
plt.title("Energy vs Frequency")
plt.grid(True)

# Plot Time Dilation vs Frequency
plt.subplot(1, 3, 3)
plt.plot(frequencies, time_dilation, label="Time Dilation", color='green')
plt.xlabel("Frequency (Hz)")
plt.ylabel("Time Dilation (t)")
plt.title("Time Dilation vs Frequency")
plt.grid(True)

plt.tight_layout()
plt.show()
