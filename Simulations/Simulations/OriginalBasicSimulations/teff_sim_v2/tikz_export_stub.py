import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

def export_plot_as_tikz(teff_field, filename="output/teff_plot.tex"):
    fig, ax = plt.subplots()
    im = ax.imshow(teff_field, cmap="plasma", origin="lower")
    plt.colorbar(im, ax=ax, label="Teff")
    plt.title("Teff Field (TikZ Export)")

    tikzplotlib.save(filename)
    plt.close()
    print(f"📄 TikZ plot exported to {filename}")

if __name__ == "__main__":
    field = np.loadtxt("output/teff_field_final.csv", delimiter=",")
    export_plot_as_tikz(field)
