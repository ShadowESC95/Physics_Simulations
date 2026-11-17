import torch
import numpy as np
from engine.entropy import compute_entropy
def evolve_teff_with_drift(field, tensor, steps, dt, lap_fn):
    field_log = []
    entropy_log = []

    for step in range(steps):
        lap = lap_fn(field)
        drift_term = torch.einsum('ijkl,ij->ij', tensor, field**2)
        dphi_dt = lap - field * (field - 1)**2 + drift_term
        field += dt * dphi_dt

        if step % 5 == 0:
            field_log.append(field.detach().cpu().numpy())
            entropy_log.append(compute_entropy(field))

    return np.array(field_log), entropy_log
