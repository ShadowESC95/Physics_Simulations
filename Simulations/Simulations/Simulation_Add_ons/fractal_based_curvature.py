
import numpy as np
import matplotlib.pyplot as plt

def fractal_curvature(x, y, recursion_depth):
    if recursion_depth == 0:
        return np.sin(x ** 2 + y ** 2)
    return fractal_curvature(x / 2, y / 2, recursion_depth - 1) * np.cos(x ** 2 + y ** 2)

if __name__ == "__main__":
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = fractal_curvature(X, Y, recursion_depth=3)
    
    plt.contourf(X, Y, Z, levels=50, cmap="viridis")
    plt.title("Fractal-Based Curvature")
    plt.colorbar()
    plt.show()
