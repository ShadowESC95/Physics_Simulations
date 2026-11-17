import sys
import os
import numpy as np
from mpi4py import MPI
import subprocess

# Set up import path for engine modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.torch.xi_chi_dual_evolver import XiChiDualEvolver
from engine.tensorboard_logger import TBLogger
from engine.observables import check_symmetry, compute_conserved_quantity

# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Simulation config
steps = 100
per_rank = steps // size
start = rank * per_rank
end = (rank + 1) * per_rank

# Initialize logger and simulation
logger = TBLogger(rank=rank)
sim = XiChiDualEvolver(logger=logger)

# Main simulation loop
for step in range(start, end):
    sim.evolve_step()
    xi, chi = sim.get_numpy()
    entropy = np.var(xi)

    # Log stats
    logger.log_field_stats(xi, chi, entropy, step)

    # Save snapshot data
    os.makedirs("output", exist_ok=True)
    np.save(f"output/xi_step_{rank}_{step}.npy", xi)
    np.save(f"output/chi_step_{rank}_{step}.npy", chi)

# Close logger
logger.close()

# Post-simulation summary (per rank)
if rank == 0:
    print("✅ Dual-field Ξχ evolution completed across ranks.")
    print("🔁 Merging logs from all ranks...")
    subprocess.run(["python3", "tools/merge_logs.py"])

# Per-rank reporting
if check_symmetry(xi):
    print(f"Rank {rank}: Symmetry OK")
else:
    print(f"Rank {rank}: Symmetry broken")

print(f"Rank {rank}: Conserved Quantity: {compute_conserved_quantity(xi, chi)}")
