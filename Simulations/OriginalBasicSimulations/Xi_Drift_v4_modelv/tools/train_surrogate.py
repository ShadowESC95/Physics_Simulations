import numpy as np
from engine.surrogate_model import FieldSurrogate

# Load simulation data
xi_data = np.load("output/xi_field_log.npy")  # Shape: (steps, H, W)
dataset = tf.data.Dataset.from_tensor_slices((xi_data[:-1], xi_data[1:])).batch(32)

# Train
model = FieldSurrogate()
model.compile(optimizer='adam')
model.fit(dataset, epochs=100)
model.save("models/surrogate_xi.h5")
