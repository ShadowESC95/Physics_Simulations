import torch
import numpy as np
from engine.utils import init_field, laplacian

def generate_dummy_drift_tensor(grid_size):
    x = torch.linspace(-1, 1, grid_size)
    y = torch.linspace(-1, 1, grid_size)
    X, Y = torch.meshgrid(x, y, indexing="ij")
    tensor = torch.exp(-10 * (X**2 + Y**2))  # Gaussian "lens"
    return tensor

def run_simulation_with_drift(grid_size=64, steps=80, dt=0.01, noise=0.02):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    phi = init_field(grid_size, noise=noise, device=device)
    drift_tensor = generate_dummy_drift_tensor(grid_size).to(device)

    log = []
    for step in range(steps):
        lap = laplacian(phi)
        correction = drift_tensor * phi  # DRIFT-modulation
        dphi_dt = lap - phi * (phi - 1)**2 + correction
        phi += dt * dphi_dt
        if step % 2 == 0:
            log.append(phi.detach().cpu().numpy())

    return log, drift_tensor.cpu().numpy()
