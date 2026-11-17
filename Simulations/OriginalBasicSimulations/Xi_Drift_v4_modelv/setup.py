from setuptools import setup, find_packages

setup(
    name="physics_simulation",
    version="3.0.0",
    description="Modular Physics Simulation Framework",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy", "scipy", "matplotlib", "pyqt5", "pyqtgraph", "h5py", 
        "pyvista", "pytest", "flake8", "black", "yaml", "yt"
    ],
    entry_points={
        "physics_sim.solvers": [
            "fenics = simulation.fenics_solver:FEniCSSolver",
            "petsc = simulation.petsc_solver:PETScSolver",
            "pysph = simulation.pysph_solver:PySPHSolver"
        ]
    },
)
