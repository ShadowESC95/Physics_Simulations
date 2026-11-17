# config.py

GRID_SIZE = 256               # Higher resolution
TIME_STEPS = 500              # Can increase up to 2000+
DT = 0.005                    # Time step
INIT_NOISE = 0.05             # ξ initial perturbation noise
DRIFT_EPSILON = 0.02          # Strength of DRIFT anisotropy
CHI_COUPLING = 0.1            # λ coupling of χ into Ξ
ENTROPY_LOG_INTERVAL = 5      # How often to log entropy
DEVICE = 'cpu'                # or 'cuda'
