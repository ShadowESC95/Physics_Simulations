import matplotlib.pyplot as plt
import numpy as np
import os

def render_drift_lensing_series(teff_log, drift_tensor, interval=10):
    os.makedirs("output/lensing_frames", exist_ok=True)
    skip = 3

    for i, frame in enumerate(teff_log):
        if i % interval != 0: continue

        plt.figure(figsize=(8, 6))
        plt.imshow(frame, cmap="magma", origin="lower")
        Y, X = np.mgrid[0:frame.shape[0], 0:frame.shape[1]]
        U = drift_tensor[..., 0, 0]
        V = drift_tensor[..., 1, 1]

        plt.quiver(X[::skip, ::skip], Y[::skip, ::skip],
                   U[::skip, ::skip], V[::skip, ::skip],
                   color="cyan", alpha=0.6)
        plt.title(f"Frame {i} with DRIFT Lensing")
        plt.savefig(f"output/lensing_frames/frame_{i:03}.png")
        plt.close()

    print("🎥 DRIFT lensing visual loop frames generated.")
