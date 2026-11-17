from abc import ABC, abstractmethod
import numpy as np

class SolverInterface(ABC):
    @abstractmethod
    def run(self) -> np.ndarray:
        pass

    @abstractmethod
    def export(self, exporter):
        pass
