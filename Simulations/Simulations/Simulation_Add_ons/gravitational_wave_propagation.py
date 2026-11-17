
import numpy as np
import matplotlib.pyplot as plt

def gravitational_wave(amplitude, frequency, time, fractal_factor):
    return amplitude * np.sin(2 * np.pi * frequency * time) * np.exp(-fractal_factor * time)

if __name__ == "__main__":
    time = np.linspace(0, 10, 1000)
    amplitude = 1.0
    frequency = 0.1
    fractal_factor = 0.05
    wave = gravitational_wave(amplitude, frequency, time, fractal_factor)
    
    plt.plot(time, wave)
    plt.title("Gravitational Wave Propagation with Fractal Factor")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()
