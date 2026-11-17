import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

def load_field(csv_path="output/teff_field_final.csv"):
    try:
        return np.loadtxt(csv_path, delimiter=",")
    except Exception as e:
        print(f"❌ Error loading Teff field: {e}")
        return None

def plot_teff_surface(field, out_path="output/teff_surface_3D.png", cmap="viridis"):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    x = np.arange(field.shape[1])
    y = np.arange(field.shape[0])
    X, Y = np.meshgrid(x, y)

    ax.plot_surface(X, Y, field, cmap=cmap, linewidth=0, antialiased=True)
    ax.set_title("3D Teff Scalar Field Surface")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Teff Value")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"🌋 Teff surface plot saved to {out_path}")

if __name__ == "__main__":
    field = load_field()
    if field is not None:
        plot_teff_surface(field)
