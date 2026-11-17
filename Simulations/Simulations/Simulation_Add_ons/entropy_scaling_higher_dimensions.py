
import numpy as np

def entropy_scaling(entropy, dimension_factor, steps):
    scaled_values = [entropy]
    for _ in range(steps):
        scaled_values.append(scaled_values[-1] * dimension_factor)
    return scaled_values

if __name__ == "__main__":
    entropy = 1.0
    dimension_factor = 1.1
    steps = 10
    results = entropy_scaling(entropy, dimension_factor, steps)
    print("Entropy Scaling in Higher Dimensions:", results)
