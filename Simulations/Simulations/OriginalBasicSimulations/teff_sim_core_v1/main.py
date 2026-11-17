import numpy as np
import os
from config import GRID_SIZE, STEPS, DT, INIT_NOISE, USE_GPU
from engine.torch_evolve import run_simulation, save_field_log_npy
from visual.animate_field import (
    plot_teff_snapshot,
    plot_entropy,
    animate_field_evolution
)

# === Run Simulation ===
print("🚀 Running scalar Teff simulation...")
field_log, entropy_log = run_simulation(
    steps=STEPS,
    grid_size=GRID_SIZE,
    dt=DT,
    use_gpu=USE_GPU,
    init_noise=INIT_NOISE
)

# === Save Raw Data ===
os.makedirs("output", exist_ok=True)
np.savetxt("output/entropy_log.csv", entropy_log, delimiter=",")
np.savetxt("output/teff_field_final.csv", field_log[-1], delimiter=",")

# ✅ Save Time-Evolving Frames as .npy Files
save_field_log_npy(field_log, folder="output/frames_data")

# === Visual Output ===
plot_teff_snapshot(field_log[-1])
plot_entropy(entropy_log, dt=DT)
animate_field_evolution(field_log, interval=150)
