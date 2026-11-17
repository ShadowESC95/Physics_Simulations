import numpy as np
from typing import List, Dict

class SimulationSolver:
    def __init__(self, config: Dict):
        self.config = config
        self.results = []

    def compute_step(self, t: float) -> float:
        # Replace legacy math with numpy for vectorized ops
        return np.sin(t * self.config.get("frequency", 1.0))

    def run(self) -> List[float]:
        self.results = [
            self.compute_step(t)
            for t in np.linspace(0, self.config.get("time_steps", 100), num=self.config.get("time_steps", 100))
        ]
        return self.results

    def export(self, exporter):
        exporter.save(self.results, filename="results.h5")
