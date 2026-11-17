import numpy as np
import matplotlib.pyplot as plt

def plot_results(results: np.ndarray):
    plt.plot(results)
    plt.title("Simulation Output")
    plt.xlabel("Time Step")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

def export_csv(results: np.ndarray, filename="output.csv"):
    np.savetxt(filename, results, delimiter=",", header="Simulation Output", comments='')
