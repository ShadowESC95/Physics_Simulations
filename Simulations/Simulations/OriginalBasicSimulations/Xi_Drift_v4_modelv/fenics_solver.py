import numpy as np
from simulation.solver_interface import SolverInterface

try:
    from dolfin import UnitSquareMesh, FunctionSpace, TrialFunction, TestFunction, solve, Function
except ImportError:
    raise ImportError("FEniCS not installed or not detected.")

class FEniCSSolver(SolverInterface):
    def __init__(self, resolution=32):
        self.resolution = resolution
        self.mesh = UnitSquareMesh(resolution, resolution)
        self.V = FunctionSpace(self.mesh, "Lagrange", 1)
        self.result = None

    def run(self) -> np.ndarray:
        u = TrialFunction(self.V)
        v = TestFunction(self.V)
        f = Function(self.V)
        a = u * v * dx
        L = f * v * dx
        self.result = Function(self.V)
        solve(a == L, self.result)
        return self.result.vector().get_local()

    def export(self, exporter):
        exporter.save(self.result.vector().get_local(), filename="fenics_output.h5")
