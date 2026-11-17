import torch
from engine.utils import init_field, laplacian
from engine.entropy import compute_entropy
import os
import numpy as np

def run_simulation(steps, grid_size, dt, use_gpu=True, init_noise=0.01):
    device = torch.device("cuda" if torch.cuda.is_available() and use_gpu else "cpu")
    phi = init_field(grid_size, noise=init_noise, device=device)

    field_log = []
    entropy_log = []

    for step in range(steps):
        lap = laplacian(phi)
        dphi_dt = lap - 2 * phi * (phi - 1)**2 + 0.1 * torch.sin(phi)
        phi += dt * dphi_dt

        field_log.append(phi.clone().detach().cpu().numpy().copy())
        entropy_log.append(compute_entropy(phi))

        if step % 10 == 0:
            print(f"🌀 Step {step}/{steps} | Entropy: {entropy_log[-1]:.4f}")

    return field_log, entropy_log


def save_field_log_npy(field_log, folder="output/frames_data"):
    """
    Saves the full field evolution log as .npy files per frame.
    """
    os.makedirs(folder, exist_ok=True)
    for i, frame in enumerate(field_log):
        np.save(os.path.join(folder, f"frame_{i:03d}.npy"), frame)
    print(f"💾 Saved {len(field_log)} frames to {folder}")
