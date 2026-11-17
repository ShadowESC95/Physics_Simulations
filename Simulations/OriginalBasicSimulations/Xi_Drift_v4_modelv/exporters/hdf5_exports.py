import h5py
import numpy as np

class HDF5Exporter:
    def save(self, data: np.ndarray, filename="results.h5"):
        with h5py.File(filename, "w") as f:
            f.create_dataset("simulation_output", data=data)
