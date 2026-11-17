
import numpy as np

def analyze_fft_phase(E_series, axis=0):
    fft_data = np.fft.fft(E_series, axis=axis)
    magnitude = np.abs(fft_data)
    phase = np.angle(fft_data)
    return magnitude, phase
