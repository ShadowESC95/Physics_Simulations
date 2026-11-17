import argparse
from simulation.config_loader import load_config
from simulation.solver_loader import load_solver
from exporters.vtk_exporter import VTKExporter
from exporters.hdf5_exporter import HDF5Exporter
from simulation.postprocess import plot_results

EXPORTERS = {
    "vtk": VTKExporter,
    "hdf5": HDF5Exporter,
}

def main():
    parser = argparse.ArgumentParser(description="Physics Simulation CLI")
    parser.add_argument("--config", type=str, required=True, help="Path to config.yaml or config.json")
    args = parser.parse_args()

    config = load_config(args.config)
    solver = load_solver(config.get("solver", "default"), **config)
    results = solver.run()

    exporter_cls = EXPORTERS.get(config.get("export_format", "hdf5"))
    if exporter_cls:
        solver.export(exporter_cls())

    plot_results(results)

if __name__ == "__main__":
    main()
