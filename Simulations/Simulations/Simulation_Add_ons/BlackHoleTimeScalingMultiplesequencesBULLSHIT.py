import numpy as np
import matplotlib.pyplot as plt
from mpmath import fibonacci

# Constants
G_0 = 6.67430e-11  # m^3 kg^-1 s^-2 (Gravitational Constant)
c_0 = 299792458  # m/s (Speed of light)
hbar = 1.054571817e-34  # J·s (Reduced Planck's constant)
kB = 1.380649e-23  # J/K (Boltzmann constant)
M_sun = 1.989e30  # kg (Solar mass)
alpha, beta = 0.1, 0.05  # Example scaling coefficients
f_P = 1.85e43  # Planck frequency (Hz)

# Frequency range (logarithmic scale)
f_range = np.logspace(30, 43, 500)

# Schwarzschild radius function with variable G, c
def schwarzschild_radius(f):
    G_f = G_0 * (1 + alpha * np.log(f / f_P))  # Variable G
    c_f = c_0 * (1 + beta * np.log(f / f_P))**-1  # Variable c
    return 2 * G_f * M_sun / c_f**2

# Standard time dilation factor
def time_dilation_standard(f, r):
    rs = schwarzschild_radius(f)
    return np.sqrt(1 - rs / r)

# Mandelbrot-based time scaling
def mandelbrot_time_scaling(f, max_iter=10):
    Z = 0 + 0j
    C = complex(f / f_P, f / f_P)
    for _ in range(max_iter):
        Z = Z**2 + C
        if abs(Z) > 2:
            break
    return max(1e-8, abs(1 + 1 / (np.real(Z) + 1e-8)))  # Ensure positive non-zero value

# Golden ratio periodic time function
phi = (1 + np.sqrt(5)) / 2
def golden_ratio_time_scaling(f):
    return max(1e-8, 1 + np.cos(2 * np.pi * f / phi))  # Ensure positive non-zero value

# Modified Pisano period-based time scaling
def pisano_period_time_scaling(f, p=24):  # Increased period for more variation
    n = int(np.log(f / f_P) * 10) % p
    fib_val = float(fibonacci(n))  # Convert mpf to float
    return max(1e-8, (fib_val % p + 1))  # Ensure positive non-zero value

# Compute different time scalings
td_standard = time_dilation_standard(f_range, schwarzschild_radius(f_range) * 2)
td_mandelbrot = np.array([mandelbrot_time_scaling(f) for f in f_range])
td_golden = np.array([golden_ratio_time_scaling(f) for f in f_range])
td_pisano = np.array([pisano_period_time_scaling(f) for f in f_range])

# Compute Entropy & Temperature Adjustments
S_standard = (kB * c_0**3 / (4 * G_0 * hbar)) * td_standard
S_mandelbrot = S_standard * td_mandelbrot
S_golden = S_standard * td_golden
S_pisano = S_standard * td_pisano

T_standard = hbar * c_0**3 / (8 * np.pi * kB * G_0 * M_sun) / td_standard
T_mandelbrot = T_standard / td_mandelbrot
T_golden = T_standard / td_golden
T_pisano = T_standard / td_pisano

# Create figure with better spacing
fig, axs = plt.subplots(3, 1, figsize=(10, 16))
plt.subplots_adjust(hspace=0.3)

# Time dilation comparison
axs[0].plot(f_range / f_P, td_standard, label="Standard", color='black', linestyle='dotted')
axs[0].plot(f_range / f_P, td_mandelbrot, label="Mandelbrot", color='blue')
axs[0].plot(f_range / f_P, td_golden, label="Golden Ratio", color='gold')
axs[0].plot(f_range / f_P, td_pisano, label="Pisano", color='red')
axs[0].set_xscale("log")
axs[0].set_yscale("log")  # Added log scale for better visualization
axs[0].set_title("Time Dilation Comparison")
axs[0].set_xlabel("f / f_P (normalized frequency)")
axs[0].set_ylabel("Time Scaling Factor")
axs[0].legend()
axs[0].grid(True)

# Entropy comparison
axs[1].plot(f_range / f_P, S_standard, label="Standard", color='black', linestyle='dotted')
axs[1].plot(f_range / f_P, S_mandelbrot, label="Mandelbrot", color='blue')
axs[1].plot(f_range / f_P, S_golden, label="Golden Ratio", color='gold')
axs[1].plot(f_range / f_P, S_pisano, label="Pisano", color='red')
axs[1].set_xscale("log")
axs[1].set_yscale("log")
axs[1].set_title("Black Hole Entropy Scaling")
axs[1].set_xlabel("f / f_P (normalized frequency)")
axs[1].set_ylabel("Entropy S_BH (scaled)")
axs[1].legend()
axs[1].grid(True)

# Temperature comparison
axs[2].plot(f_range / f_P, T_standard, label="Standard", color='black', linestyle='dotted')
axs[2].plot(f_range / f_P, T_mandelbrot, label="Mandelbrot", color='blue')
axs[2].plot(f_range / f_P, T_golden, label="Golden Ratio", color='gold')
axs[2].plot(f_range / f_P, T_pisano, label="Pisano", color='red')
axs[2].set_xscale("log")
axs[2].set_yscale("log")
axs[2].set_title("Black Hole Temperature Scaling")
axs[2].set_xlabel("f / f_P (normalized frequency)")
axs[2].set_ylabel("Temperature T_BH (scaled)")
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()