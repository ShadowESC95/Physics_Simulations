import numpy as np
import h5py

xi = np.random.rand(64, 64, 64) * 1e-9  # yt likes small physical values

with h5py.File("data/xi_yt_dataset.h5", "w") as f:
    f.create_dataset("/density", data=xi)
    f.attrs["yt_fields"] = "density"
    f.attrs["yt_grid_dimensions"] = [64, 64, 64]
    f.attrs["yt_domain_dimensions"] = [64, 64, 64]
    f.attrs["yt_domain_left_edge"] = [0.0, 0.0, 0.0]
    f.attrs["yt_domain_right_edge"] = [1.0, 1.0, 1.0]
