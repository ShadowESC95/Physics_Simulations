import yt
import numpy as np

xi = np.load("output/xi_field_log.npy")[-1]  # Last frame
data = {"xi": (xi, "dimensionless")}

bbox = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
ds = yt.load_uniform_grid(data, xi.shape, length_unit="m", bbox=bbox)

slc = yt.SlicePlot(ds, "z", "xi")
slc.save("yt_slice.png")

vol = yt.VolumeRendering(ds, "xi")
vol.save("yt_volume.png")
