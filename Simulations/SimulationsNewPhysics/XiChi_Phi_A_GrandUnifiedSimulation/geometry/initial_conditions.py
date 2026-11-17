import numpy as np

def initialize_fields(config):
    shape = tuple(config.get("grid_shape", [64, 64, 64]))
    timesteps = config.get("timesteps", 100)

    phi = np.zeros((timesteps, *shape))
    A_mu = np.zeros((timesteps, *shape, 4))  # 4-vector field A_μ

    # Same for Xi and chi...
    fields = {
        "phi": phi,
        "A_mu": A_mu,
        "Xi": np.zeros_like(phi),
        "chi": np.zeros_like(phi),
    }

    return fields

