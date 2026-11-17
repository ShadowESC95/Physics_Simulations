import numpy as np
def apply_kerr_nonlinearity(epsilon_tensor, E_field, chi3=0.001):
    return epsilon_tensor + chi3 * np.square(E_field)
