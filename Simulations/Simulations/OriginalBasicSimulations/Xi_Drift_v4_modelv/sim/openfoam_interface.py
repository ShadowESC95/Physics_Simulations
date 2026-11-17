import numpy as np
try:
    import openfoam_bridge
except ImportError:
    openfoam_bridge = None

def run_openfoam_cfd(time_steps: int, frequency: float) -> np.ndarray:
    if openfoam_bridge is None:
        raise ImportError("OpenFOAM bridge module not compiled.")
    return np.array(openfoam_bridge.run_openfoam_simulation(time_steps, frequency))
