import os
import numpy as np
from torch.utils.tensorboard import SummaryWriter

class TBLogger:
    def __init__(self, rank=0):
        self.writer = SummaryWriter(log_dir=f"logs/rank_{rank}")
        self.rank = rank

    def log_scalar(self, tag, value, step):
        self.writer.add_scalar(tag, value, step)

    def log_field_stats(self, xi, chi, entropy, step):
        self.writer.add_scalar("Xi/Mean", np.mean(xi), step)
        self.writer.add_scalar("Xi/Std", np.std(xi), step)
        self.writer.add_scalar("Chi/Mean", np.mean(chi), step)
        self.writer.add_scalar("Chi/Std", np.std(chi), step)
        self.writer.add_scalar("Entropy/Value", entropy, step)

        # Derived metrics
        energy = np.sum(xi**2 + chi**2)
        symmetry = np.var(xi - chi)
        drift = np.mean(np.gradient(xi))

        self.writer.add_scalar("Observables/Total Energy", energy, step)
        self.writer.add_scalar("Observables/Symmetry Breaking", symmetry, step)
        self.writer.add_scalar("Observables/Drift Magnitude", drift, step)

    def close(self):
        self.writer.close()
