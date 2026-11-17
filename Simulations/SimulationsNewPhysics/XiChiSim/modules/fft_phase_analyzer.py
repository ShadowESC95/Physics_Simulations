import numpy as np

def analyze_fft_phase(signal, dt=1.0, detrend=True, window=True):
    x = np.asarray(signal, dtype=float)
    if detrend:
        x = x - np.mean(x)
    if window:
        x = x * np.hanning(len(x))
    spec = np.fft.rfft(x)
    mag = np.abs(spec)
    phase = np.angle(spec)
    freqs = np.fft.rfftfreq(len(x), d=dt)
    return mag, phase, freqs
