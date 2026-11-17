import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

def overlay_drift_tensor(field, tensor, out_path=None):
    os.makedirs("output", exist_ok=True)
    if out_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"output/teff_drift_overlay_{timestamp}.png"

    plt.figure(figsize=(7, 6))
    plt.imshow(field, cmap='plasma', origin='lower')
    Y, X = np.mgrid[0:field.shape[0], 0:field.shape[1]]
    plt.quiver(X, Y, tensor[0], tensor[1], color='white', alpha=0.7, scale=20)
    plt.title("Teff Field with DRIFT Tensor Overlay")
    plt.colorbar(label="Teff")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"🌐 Drift overlay saved to {out_path}")
