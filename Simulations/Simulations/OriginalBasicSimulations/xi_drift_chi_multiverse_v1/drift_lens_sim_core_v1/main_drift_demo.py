import numpy as np
from drift_lensing_overlay import save_drift_overlay

# Load pre-generated Teff and DRIFT fields
teff_field = np.loadtxt("output/teff_field_final.csv", delimiter=",")
drift_tensor = np.load("output/dummy_drift_tensor.npy")

save_drift_overlay(teff_field, drift_tensor)

from modules.drift_lensing_animator import animate_drift_overlay

animate_drift_overlay(field_log, drift_tensor)
