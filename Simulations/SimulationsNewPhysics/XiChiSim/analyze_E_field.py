# go to project root (one level up)
cd $HOME/Desktop/Physics/Simulations/SimulationsNewPhysics/xi_chi_fenicsx_gui_env

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

# create the analyzer only if it doesn't exist yet
test -f analyze_E_field.py || cat > analyze_E_field.py <<'PY'
import os, h5py, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from modules.polarization_tracker import compute_polarization_metrics
from modules.fft_phase_analyzer import analyze_fft_phase
from modules.recursive_loop_detector import detect_recursive_loops

IN_PATH="outputs/E_field.h5"; DS="E_field"; OUT="outputs/visualizations"
os.makedirs(OUT, exist_ok=True)
with h5py.File(IN_PATH,"r") as f:
    if DS not in f: raise KeyError(f"Dataset '{DS}' not found; keys={list(f.keys())}")
    arr = f[DS][()]

def to_vec3_block(a):
    a = np.asarray(a)
    if a.ndim==3: return np.stack([a,a,a], axis=-1)
    if a.ndim==4 and a.shape[-1] in (2,3):
        if a.shape[-1]==2:
            pad = np.zeros(a.shape[:-1]+(1,), a.dtype); a = np.concatenate([a,pad], axis=-1)
        return a
    if a.ndim==4: return np.stack([a[0],a[0],a[0]], axis=-1)
    if a.ndim==5:
        b=a[0]; 
        if b.shape[-1]==2:
            pad = np.zeros(b.shape[:-1]+(1,), b.dtype); b = np.concatenate([b,pad], axis=-1)
        return b
    raise ValueError(f"Unsupported E_field dims: {a.shape}")

E = to_vec3_block(arr)
mag, div, curl_mag = compute_polarization_metrics(E)
zmid = (mag.shape[2]//2) if mag.ndim==3 else 0

plt.imshow(mag[:,:,zmid].T, origin="lower", aspect="auto"); plt.title("Polarization Magnitude (Z mid)")
plt.colorbar(); plt.tight_layout(); plt.savefig(os.path.join(OUT,"polarization_ellipse.png"), dpi=200); plt.clf()

cx, cy = mag.shape[0]//2, mag.shape[1]//2
line = mag[cx, cy, :] if mag.ndim==3 else mag[cx, :]
mag_fft, phase_fft, freqs = analyze_fft_phase(line, dt=1.0)
plt.plot(freqs, mag_fft); plt.xlabel("freq"); plt.ylabel("|FFT|"); plt.title("FFT (central line)")
plt.tight_layout(); plt.savefig(os.path.join(OUT,"fft_spectrum.png"), dpi=200); plt.clf()

dE = np.gradient(line); plt.plot(line, dE, lw=0.8)
plt.xlabel("E"); plt.ylabel("dE/dξ"); plt.title("Phase-space: E vs dE/dξ")
plt.tight_layout(); plt.savefig(os.path.join(OUT,"phase_space_E_vs_dEdx.png"), dpi=200); plt.clf()

peaks, ac = detect_recursive_loops(line, thresh=0.75, min_sep=5)
import matplotlib.pyplot as plt
plt.bar(range(len(ac)), ac, width=1.0)
for L,_ in peaks: plt.axvline(L, ls="--", lw=0.6)
plt.xlabel("Lag"); plt.ylabel("Norm. autocorr"); plt.title("Recursive re-alignment")
plt.tight_layout(); plt.savefig(os.path.join(OUT,"recursive_heatmap.png"), dpi=200); plt.clf()
print(f"[ok] wrote -> {OUT}")
PY

# run it (stay in project root)
python analyze_E_field.py
ls -lh outputs/visualizations
