import yt
import numpy as np

def render_3d_field():
    xi = np.load("output/xi_field_log.npy")  # Shape: (T, H, W)
    
    # Convert to yt dataset (3D grid)
    data = dict(density=(xi[-1], "g/cm**3"))  # Example unit
    bbox = np.array([[-10., 10.], [-10., 10.], [-10., 10.]])
    ds = yt.load_uniform_grid(data, xi.shape[1:], bbox=bbox)
    
    # Volume rendering
    sc = yt.create_scene(ds, field='density')
    sc.show()
