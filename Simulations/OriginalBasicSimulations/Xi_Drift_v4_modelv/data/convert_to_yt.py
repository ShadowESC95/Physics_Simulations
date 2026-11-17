import yt
import numpy as np
import os

def create_yt_dataset(output_dir="output", filename="xi_yt_dataset.h5"):
    xi = np.load(os.path.join(output_dir, "xi_field_log.npy"))
    chi = np.load(os.path.join(output_dir, "chi_field_log.npy"))
    drift = np.load(os.path.join(output_dir, "drift_tensor_Xi.npy"))

    data = {
        ('gas', 'Xi'): (xi[-1], 'code_length'),
        ('gas', 'Chi'): (chi[-1], 'code_length'),
        ('gas', 'Drift_x'): (drift[-1,:,:,0], 'code_velocity'),
        ('gas', 'Drift_y'): (drift[-1,:,:,1], 'code_velocity')
    }

    bbox = np.array([[0.0, 1.0], [0.0, 1.0]])
    ds = yt.load_uniform_grid(data, xi[-1].shape, length_unit="cm", bbox=bbox, nprocs=1)
    ds.save_as_dataset(filename=os.path.join(output_dir, filename), fields=data.keys())

if __name__ == "__main__":
    create_yt_dataset()
