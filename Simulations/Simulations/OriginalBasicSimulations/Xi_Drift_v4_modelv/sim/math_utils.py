import numpy as np
from typing import Union

def square(x: Union[int, float, np.ndarray]) -> Union[int, float, np.ndarray]:
    return np.square(x)

def normalize_array(arr: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(arr)
    return arr / norm if norm != 0 else arr
