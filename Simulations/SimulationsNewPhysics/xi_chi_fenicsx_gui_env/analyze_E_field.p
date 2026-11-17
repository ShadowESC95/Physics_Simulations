import os, h5py, numpy as np, matplotlib.pyplot as plt
from modules.polarization_tracker import compute_polarization_metrics
from modules.fft_phase_analyzer import analyze_fft_phase
from modules.recursive_loop_detector import detect_recursive_loops

IN_PATH  = "outputs/E_field.h5"
DS_NAME  = "E_field"
OUT_DIR  = "outputs/visualizations"
os.makedirs(OUT_DIR, exist_ok=True)

with h5py.File(IN_PATH, "r") as f:
    ds = f[DS_NAME]
    shape = ds.shape

# Heuristic parse of dataset layout -> make a 3D vector field block E3d (...,3)
def to_3d_vector_block(arr):
    arr = np.asarray(arr)
    if arr.ndim == 3:
        # scalar on 3D grid -> fake vector (same in xyz)
        return np.stack([arr, arr, arr], axis=-1)
    if arr.ndim == 4:
        # Either (Nx,Ny,Nz,3) vector OR (T,Nx,Ny,Nz) scalar time series
        if arr.shape[-1] in (3, 2):
            if arr.shape[-1] == 2:  # pad to 3
                pad = np.zeros(arr.shape[:-1] + (1,), arr.dtype)
                arr = np.concatenate([arr, pad], axis=-1)
            return arr
        else:
            return np.stack([arr[0], arr[0], arr[0]], axis=-1)  # first time slice
    if arr.ndim == 5:
        # (T,Nx,Ny,Nz,3) -> first time
        blk = arr[0]
        if blk.shape[-1] == 2:
            pad = np.zeros(blk.shape[:-1] + (1,), blk.dtype)
            blk = np.concatenate([blk, pad], axis=-1)
        return blk
    raise ValueError(f"Unsupported E_field dims: {arr.shape}")

with h5py.File(IN_PATH, "r") as f:
    Eds = f[DS_NAME]
    # Load conservatively (not [:]) to avoid huge RAM spikes
    data = Eds[()]  # small file in your tree; adjust to slicing if needed

E3d = to_3d_vector_block(data)           # (Nx,Ny,Nz,3) or (Nx,Ny,3)
nxny = E3d.shape[:2]
nz = E3d.shape[2] if E3d.ndim >= 4 else 1

# --- Polarization metrics ---
mag, div, curl_mag = compute_polarization_metrics(E3d)
zmid = (nz // 2) if nz > 1 else 0

plt.imshow(mag[:, :, zmid].T, origin="lower", aspect="auto")
plt.title("Polarization Magnitude (Z mid-slice)")
plt.colorbar()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "polarization_ellipse.png"), dpi=200)
plt.clf()

# --- FFT (spatial or temporal, depending on your data) ---
# Use a line through the volume; default: central x,y across the last axis
cx, cy = (mag.shape[0] // 2), (mag.shape[1] // 2)
line = mag[cx, cy, :] if mag.ndim == 3 else mag[cx, :]  # fall back for 2D

mag_fft, phase_fft, freqs = analyze_fft_phase(line, dt=1.0)
plt.plot(freqs, mag_fft)
plt.xlabel("Frequency (arb.)")
plt.ylabel("|FFT|")
plt.title("FFT Spectrum (central line)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fft_spectrum.png"), dpi=200)
plt.clf()

# --- Phase-space E vs dE/dt (or dE/dz if spatial line) ---
dE = np.gradient(line)
plt.plot(line, dE, lw=0.8)
plt.xlabel("E")
plt.ylabel("dE/dξ")  # ξ = t or z depending on your data
plt.title("Phase-Space Trajectory: E vs dE/dξ")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "phase_space_E_vs_dEdx.png"), dpi=200)
plt.clf()

# --- Recursive loop detection ---
peaks, ac = detect_recursive_loops(line, thresh=0.75, min_sep=5)
lags = [p for p, _ in peaks]
plt.bar(range(len(ac)), ac, width=1.0)
for L in lags:
    plt.axvline(L, ls="--", lw=0.6)
plt.xlabel("Lag")
plt.ylabel("Normalized autocorrelation")
plt.title("Recursive Re-alignment (autocorr + detected lags)")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "recursive_heatmap.png"), dpi=200)
plt.clf()

print(f"[done] wrote PNGs to: {OUT_DIR}")
