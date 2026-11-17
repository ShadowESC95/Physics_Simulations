import h5py
import numpy as np

with h5py.File("E_field.h5", "r") as f:
    keys = list(f.keys())
    print("HDF5 keys:", keys)
    
    if not keys:
        print("No datasets found.")
        exit()

    data = f[keys[0]][()]
    print("Shape:", data.shape)
    print("Min value:", np.min(data))
    print("Max value:", np.max(data))
    print("Mean value:", np.mean(data))

