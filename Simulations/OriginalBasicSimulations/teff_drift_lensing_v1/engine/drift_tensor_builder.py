import numpy as np

def compute_tensor(teff_field):
    """Compute DRIFT tensor as pseudo-gradient of Teff."""
    dy, dx = np.gradient(teff_field)
    
    # Normalize the tensor for stability
    norm = np.sqrt(dx**2 + dy**2) + 1e-8
    dx /= norm
    dy /= norm
    
    return np.stack((dx, dy))  # shape (2, H, W)

def save_tensor(tensor, out_path="output/drift_tensor.npy"):
    np.save(out_path, tensor)
    print(f"🧲 DRIFT tensor saved to {out_path}")
