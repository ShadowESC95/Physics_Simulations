import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.fft import fft2, fftshift

# --- Generate synthetic 2D field snapshots (replace with your data if needed) ---
N_snapshots = 20
field_shape = (64, 64)
np.random.seed(42)
xi_fields = []
xi = np.random.randn(*field_shape) * 0.1
for _ in range(N_snapshots):
    xi += 0.03 * np.random.randn(*field_shape) + 0.04 * np.sin(np.linspace(0, np.pi, field_shape[0]))[:, None]
    xi_fields.append(np.copy(xi))
xi_fields = np.array(xi_fields)  # Shape: (N_snapshots, 64, 64)

# --- FFT and mask definitions ---
fft_spectra = [np.abs(fftshift(fft2(xi))) for xi in xi_fields]

shape = xi_fields[0].shape
center = np.array(shape) // 2
yy, xx = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), indexing='ij')
r2 = (xx - center[1])**2 + (yy - center[0])**2

radius_low = 6      # low-frequency circle
radius_high = 20    # inner radius of high-frequency annulus

low_mask = r2 < radius_low**2
mid_mask = (r2 >= radius_low**2) & (r2 < radius_high**2)
high_mask = r2 >= radius_high**2

low_freq_energy = []
mid_freq_energy = []
high_freq_energy = []
total_energy = []

for spectrum in fft_spectra:
    energy = spectrum**2
    low_freq_energy.append(np.sum(energy[low_mask]))
    mid_freq_energy.append(np.sum(energy[mid_mask]))
    high_freq_energy.append(np.sum(energy[high_mask]))
    total_energy.append(np.sum(energy))

low_freq_energy = np.array(low_freq_energy)
mid_freq_energy = np.array(mid_freq_energy)
high_freq_energy = np.array(high_freq_energy)
total_energy = np.array(total_energy)

# --- Initial and final values & ratios ---
init = 0
final = -1

spectral_summary = {
    "initial_low_freq_energy": float(low_freq_energy[init]),
    "final_low_freq_energy": float(low_freq_energy[final]),
    "initial_mid_freq_energy": float(mid_freq_energy[init]),
    "final_mid_freq_energy": float(mid_freq_energy[final]),
    "initial_high_freq_energy": float(high_freq_energy[init]),
    "final_high_freq_energy": float(high_freq_energy[final]),
    "initial_total_energy": float(total_energy[init]),
    "final_total_energy": float(total_energy[final]),
    "low_freq_frac_init": float(low_freq_energy[init] / total_energy[init]),
    "low_freq_frac_final": float(low_freq_energy[final] / total_energy[final]),
    "mid_freq_frac_init": float(mid_freq_energy[init] / total_energy[init]),
    "mid_freq_frac_final": float(mid_freq_energy[final] / total_energy[final]),
    "high_freq_frac_init": float(high_freq_energy[init] / total_energy[init]),
    "high_freq_frac_final": float(high_freq_energy[final] / total_energy[final]),
    "high_to_low_energy_ratio_init": float(high_freq_energy[init] / low_freq_energy[init]),
    "high_to_low_energy_ratio_final": float(high_freq_energy[final] / low_freq_energy[final])
}

print("Spectral summary (initial vs final):")
for k, v in spectral_summary.items():
    print(f"{k:35s}: {v:.4f}")

# --- Optional: plot energy in each band over time ---
plt.figure(figsize=(9, 6))
plt.plot(low_freq_energy, label='Low frequency')
plt.plot(mid_freq_energy, label='Mid frequency')
plt.plot(high_freq_energy, label='High frequency')
plt.plot(total_energy, label='Total', linestyle='--', color='gray')
plt.xlabel('Snapshot (time step)')
plt.ylabel('Energy')
plt.title('Spectral Energy Evolution')
plt.legend()
plt.tight_layout()
plt.savefig("Spectral_Energy_Evolution.png")
plt.show()

