# config.py

# === Simulation Parameters ===
GRID_SIZE = 128         # Grid dimensions (NxN)
STEPS = 800             # Total evolution steps
DT = 0.01               # Timestep size
INIT_NOISE = 0.02       # Initial noise in scalar field
USE_GPU = True          # Use CUDA if available

# === Output Settings ===
SAVE_INTERVAL = 5       # Interval for saving snapshots
OUTPUT_DIR = "output"
