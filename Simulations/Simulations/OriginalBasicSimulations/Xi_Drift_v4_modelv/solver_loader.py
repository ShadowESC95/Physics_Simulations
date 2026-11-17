def load_solver(name: str, **kwargs):
    if name == "fenics":
        from simulation.fenics_solver import FEniCSSolver
        return FEniCSSolver(**kwargs)
    elif name == "petsc":
        from simulation.petsc_solver import PETScSolver
        return PETScSolver(**kwargs)
    elif name == "pysph":
        from simulation.pysph_solver import PySPHSolver
        return PySPHSolver(**kwargs)
    else:
        from simulation.solver import SimulationSolver
        return SimulationSolver(**kwargs)
