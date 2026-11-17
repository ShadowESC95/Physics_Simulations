# config.py
GRID_SIZE = 256
TIME_STEPS = 1000         # Increased for proper recursive depth
DT = 0.002                # Stability boost
DRIFT_EPSILON = 0.02
CHI_COUPLING = 0.1
ENTROPY_LOG_INTERVAL = 1
DEVICE = 'cpu'  # Change to 'cuda' if available
