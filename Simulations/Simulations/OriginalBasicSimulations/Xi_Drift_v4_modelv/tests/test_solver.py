import pytest
import numpy as np
from simulation.solver import SimulationSolver

def test_simulation_output_shape():
    solver = SimulationSolver({"time_steps": 100, "frequency": 0.1})
    results = solver.run()
    assert len(results) == 100

def test_simulation_output_type():
    solver = SimulationSolver({"time_steps": 10, "frequency": 1.0})
    results = solver.run()
    assert all(isinstance(r, float) for r in results)
