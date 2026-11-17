from sim.solver import SimulationSolver
from sim.config_loader import CONFIG
from exporters.hdf5_exports import HDF5Exporter
from utils.logger import setup_logger  # Make sure this exists

logger = setup_logger("simulation")

def main():
    logger.info("Initializing Simulation")
    solver = SimulationSolver(CONFIG)
    results = solver.run()
    solver.export(HDF5Exporter())
    logger.info("Simulation complete. Results saved.")

if __name__ == "__main__":
    main()

