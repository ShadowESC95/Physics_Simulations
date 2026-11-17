import torch

class XiEvolver:
    def __init__(self, shape=(64, 64), device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.xi = torch.rand(shape, device=self.device)
        self.dx = 1.0
        self.kappa = 1.0  # For photon mass calc

    def evolve_step(self):
        laplacian = -4 * self.xi
        laplacian += torch.roll(self.xi, shifts=1, dims=0)
        laplacian += torch.roll(self.xi, shifts=-1, dims=0)
        laplacian += torch.roll(self.xi, shifts=1, dims=1)
        laplacian += torch.roll(self.xi, shifts=-1, dims=1)

        self.xi = self.xi + 0.01 * laplacian

    def get_numpy(self):
        return self.xi.detach().cpu().numpy()

    def photon_mass_squared(self):
        grad = torch.gradient(self.xi)[0]  # simple approximation
        return self.kappa * torch.norm(grad)**2
