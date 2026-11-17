
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Load data: columns = wavelength (um), n, k
data = np.loadtxt("Si_data.txt", skiprows=1)
wavelengths, n, k = data[:,0], data[:,1], data[:,2]

# Compute complex permittivity
epsilon_complex = (n + 1j*k)**2

# Interpolation (returns complex permittivity for any λ)
epsilon_interp = interp1d(wavelengths, epsilon_complex, kind='cubic', bounds_error=False, fill_value="extrapolate")

# Example usage:
λ_query = np.linspace(0.4, 1.6, 500)
ε_query = epsilon_interp(λ_query)

plt.plot(λ_query, np.real(ε_query), label='Re(ε)')
plt.plot(λ_query, np.imag(ε_query), label='Im(ε)')
plt.xlabel("Wavelength (µm)")
plt.ylabel("ε")
plt.legend()
plt.title("Interpolated ε(λ) from real material data")
plt.grid(True)
plt.tight_layout()
plt.savefig("epsilon_fit_plot.png")
