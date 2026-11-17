
import numpy as np
import h5py
import matplotlib.pyplot as plt
from modules.polarization_tracker import compute_polarization_metrics
from modules.fft_phase_analyzer import analyze_fft_phase
from modules.recursive_loop_detector import detect_recursive_loops

def load_field(filename):
    with h5py.File(filename, 'r') as f:
        return np.array(f['E_field'])

def plot_polarization_ellipses(E, out_path):
    magnitude, divergence, curl = compute_polarization_metrics(E)
    slice_mag = magnitude[:, :, E.shape[2]//2]
    plt.imshow(slice_mag.T, origin='lower', cmap='viridis')
    plt.colorbar(label='|E|')
    plt.title("Polarization Magnitude Ellipse Cross-Section")
    plt.savefig(out_path / 'polarization_ellipse.png')
    plt.close()

def plot_fft_spectrogram(E_series, out_path):
    mag, phase = analyze_fft_phase(np.array(E_series), axis=0)
    plt.imshow(np.log1p(mag[:, 0, 0]), cmap='magma', aspect='auto')
    plt.title("FFT Spectrogram at (0,0)")
    plt.xlabel("Time Step")
    plt.ylabel("Frequency Component")
    plt.colorbar()
    plt.savefig(out_path / 'fft_spectrogram.png')
    plt.close()

def plot_phase_space(E_series, dt, out_path):
    E_t = np.array(E_series)
    dE_dt = (E_t[1:] - E_t[:-1]) / dt
    i, j, k = 0, 0, 0
    E_val = E_t[:, i, j, k, 0]
    dE_val = dE_dt[:, i, j, k, 0]
    plt.plot(E_val[:-1], dE_val)
    plt.title("E vs dE/dt Phase-Space (x-comp @ 0,0,0)")
    plt.xlabel("E")
    plt.ylabel("dE/dt")
    plt.savefig(out_path / 'phase_space_E_vs_dEdt.png')
    plt.close()

def plot_recursive_heatmap(E_series, out_path):
    spikes = detect_recursive_loops(E_series)
    heatmap = np.zeros(len(E_series))
    for t, _ in spikes:
        heatmap[t] += 1
    plt.plot(heatmap)
    plt.title("Recursive Phase Spike Timeline")
    plt.xlabel("Time")
    plt.ylabel("Spikes")
    plt.savefig(out_path / 'recursive_heatmap.png')
    plt.close()

def main():
    out_path = Path("outputs/visualizations")
    out_path.mkdir(parents=True, exist_ok=True)

    field_data = load_field("outputs/E_field.h5")
    E_series = [field_data for _ in range(20)]  # mock time series
    dt = 0.1

    plot_polarization_ellipses(field_data, out_path)
    plot_fft_spectrogram(E_series, out_path)
    plot_phase_space(E_series, dt, out_path)
    plot_recursive_heatmap(E_series, out_path)

if __name__ == "__main__":
    main()
