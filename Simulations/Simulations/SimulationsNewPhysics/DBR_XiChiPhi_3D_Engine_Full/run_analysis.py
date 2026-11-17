
import h5py
import numpy as np
import matplotlib.pyplot as plt
from modules.polarization_tracker import compute_polarization_metrics
from modules.fft_phase_analyzer import analyze_fft_phase
from modules.recursive_loop_detector import detect_recursive_loops

data = h5py.File("outputs/E_field.h5", "r")["E_field"][:]

# Polarization metrics
mag, div, curl = compute_polarization_metrics(np.stack([data]*3, axis=-1))
plt.imshow(mag[:, :, data.shape[2]//2])
plt.title("Polarization Magnitude (Z slice)")
plt.savefig("outputs/visualizations/polarization_ellipse.png")
plt.clf()

# FFT
E_series = data[data.shape[0]//2, data.shape[1]//2, :]
mag_fft, phase_fft = analyze_fft_phase(E_series)
plt.plot(mag_fft)
plt.title("FFT Spectrum (central point)")
plt.savefig("outputs/visualizations/fft_spectrogram.png")
plt.clf()

# E vs dE/dt
dE = np.gradient(E_series)
plt.plot(E_series, dE)
plt.title("Phase-Space Trajectory: E vs dE/dt")
plt.savefig("outputs/visualizations/phase_space_E_vs_dEdt.png")
plt.clf()

# Recursive detection
loops = detect_recursive_loops(E_series)
loop_times = [t for t, _ in loops]
plt.hist(loop_times, bins=20)
plt.title("Recursive Re-alignment Heatmap")
plt.savefig("outputs/visualizations/recursive_heatmap.png")
