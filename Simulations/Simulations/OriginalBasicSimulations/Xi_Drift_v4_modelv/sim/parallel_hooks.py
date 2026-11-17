from mpi4py import MPI
import numpy as np

def distributed_simulation(local_steps: int, omega: float):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    local_result = np.sin(np.linspace(rank * local_steps, (rank + 1) * local_steps, local_steps) * omega)
    all_results = comm.gather(local_result, root=0)

    if rank == 0:
        return np.concatenate(all_results)
    return None
