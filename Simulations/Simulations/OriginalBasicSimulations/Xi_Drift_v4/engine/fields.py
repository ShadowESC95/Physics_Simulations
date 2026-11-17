# engine/fields.py

import numpy as np

def generate_initial_field(shape=(128, 128), noise=0.01, base=1.0):
    field = np.full(shape, base, dtype=np.float32)
    field += noise * np.random.randn(*shape).astype(np.float32)
    return field

# Initial Xi and Chi fields (static setup)
xi_field = generate_initial_field()
chi_field = generate_initial_field(base=0.0)

