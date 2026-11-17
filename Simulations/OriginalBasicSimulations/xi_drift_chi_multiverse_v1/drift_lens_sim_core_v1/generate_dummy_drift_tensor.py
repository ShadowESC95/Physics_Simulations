import numpy as np
import os

def generate_dummy_drift_tensor(shape=(128, 128), frequency=6):
    """
    Fake DRIFT tensor field (sinusoidal) for visual testing.
    """
    x = np.linspace(0, 2 * np.pi, shape[0])
    y = np.linspace(0, 2 * np.pi, shape[1])
    X, Y = np.meshgrid(x, y)
    drift_tensor = 0.5 * (np.sin(frequency * X) * np.cos(frequency * Y))
    return drift_tensor

if __name__ == "__main__":
    tensor = generate_dummy_drift_tensor()
    np.save("output/dummy_drift_tensor.npy", tensor)
    print("💾 Dummy DRIFT tensor saved to output/dummy_drift_tensor.npy")
