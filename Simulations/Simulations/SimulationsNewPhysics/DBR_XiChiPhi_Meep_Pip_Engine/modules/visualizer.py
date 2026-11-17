import h5py
def save_h5_field(data, filename):
    with h5py.File(filename, "w") as f:
        f.create_dataset("E_field", data=data)
