
import numpy as np

def chiral_tensor_field(shape, chiral_strength=0.05):
    epsilon_tensor = np.zeros((*shape, 3, 3))
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                angle = 2 * np.pi * (i + j + k) / sum(shape)
                R = np.array([
                    [np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1]
                ])
                epsilon_tensor[i, j, k] = np.identity(3) + chiral_strength * R
    return epsilon_tensor
