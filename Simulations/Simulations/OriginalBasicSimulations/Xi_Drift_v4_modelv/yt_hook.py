import numpy as np
import yt

def view_with_yt(data: np.ndarray):
    ds = yt.load_uniform_grid(
        {"density": data},
        data.shape,
        length_unit="cm",
        bbox=np.array([[0, data.shape[0]], [0, data.shape[1]], [0, 1]])
    )
    slc = yt.SlicePlot(ds, "z", "density")
    slc.show()
