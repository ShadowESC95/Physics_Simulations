import numpy as np
from simulation.solver_interface import SolverInterface

try:
    from petsc4py import PETSc
except ImportError:
    raise ImportError("PETSc4Py not found")

class PETScSolver(SolverInterface):
    def __init__(self, size=100):
        self.size = size
        self.result = None

    def run(self) -> np.ndarray:
        A = PETSc.Mat().createAIJ([self.size, self.size])
        A.setFromOptions()
        A.setUp()

        x = PETSc.Vec().createSeq(self.size)
        b = PETSc.Vec().createSeq(self.size)
        b.set(1.0)

        ksp = PETSc.KSP().create()
        ksp.setOperators(A)
        ksp.solve(b, x)

        self.result = x.getArray()
        return self.result

    def export(self, exporter):
        exporter.save(self.result, filename="petsc_output.h5")
