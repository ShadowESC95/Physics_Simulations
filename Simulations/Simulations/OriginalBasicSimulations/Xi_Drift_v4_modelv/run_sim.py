from sim.solver import SimulationSolver
from sim.config_loader import CONFIG

xi_sim = SimulationSolver(CONFIG)
xi_sim.run()  # Or .evolve_step() if that’s what you want

