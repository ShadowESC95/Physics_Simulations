
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def load_nk(file):
    data = np.loadtxt(file, skiprows=1)
    wl, n, k = data[:,0], data[:,1], data[:,2]
    epsilon = (n + 1j*k)**2
    return wl, epsilon

def interpolate_epsilon(wl, epsilon):
    return interp1d(wl, epsilon, kind='cubic', bounds_error=False, fill_value="extrapolate")

def save_epsilon(wl, eps_interp, filename):
    wl_dense = np.linspace(wl.min(), wl.max(), 1000)
    eps_vals = eps_interp(wl_dense)
    np.save(filename, eps_vals)
    return wl_dense, eps_vals

def plot_epsilon(wl_dense, eps_vals, label):
    plt.plot(wl_dense, np.real(eps_vals), label=f"Re(ε) {label}")
    plt.plot(wl_dense, np.imag(eps_vals), label=f"Im(ε) {label}")

# Example usage
files = ['Si_nk.txt', 'GaAs_nk.txt', 'SiO2_nk.txt']
for f in files:
    wl, eps = load_nk(f)
    interp = interpolate_epsilon(wl, eps)
    wl_dense, eps_vals = save_epsilon(wl, interp, f.replace('.txt', '.npy'))
    plot_epsilon(wl_dense, eps_vals, f.replace('_nk.txt',''))

plt.xlabel("Wavelength (µm)")
plt.ylabel("Permittivity ε")
plt.title("Interpolated Dielectric Functions")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("dielectric_fits.png")
