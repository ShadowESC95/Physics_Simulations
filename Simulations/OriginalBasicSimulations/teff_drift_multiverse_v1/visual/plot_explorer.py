import matplotlib.pyplot as plt
import numpy as np

def export_plot_as_vector(teff_field, use_tikz=True):
    try:
        if use_tikz:
            import tikzplotlib
            plt.imshow(teff_field, cmap='inferno', origin='lower')
            tikzplotlib.save("output/teff_field_plot.tex")
            print("📦 Saved TikZ LaTeX vector plot.")
        else:
            raise ImportError
    except:
        plt.imshow(teff_field, cmap='inferno', origin='lower')
        plt.savefig("output/teff_field_plot.pdf")
        print("📄 PDF fallback export used.")
