from simulation.solver_interface import SolverInterface
import numpy as np

try:
    from pysph.base.kernels import CubicSpline
    from pysph.base.nnps import DomainManager
    from pysph.base.utils import get_particle_array
except ImportError:
    raise ImportError("PySPH not installed.")

class PySPHSolver(SolverInterface):
    def __init__(self, num_particles=100):
        self.num_particles = num_particles
        self.result = None

    def run(self) -> np.ndarray:
        x = np.linspace(0, 1, self.num_particles)
        pa = get_particle_array(name='fluid', x=x)
        self.result = pa.x.copy()
        return self.result

    def export(self, exporter):
        exporter.save(self.result, filename="pysph_output.csv")
