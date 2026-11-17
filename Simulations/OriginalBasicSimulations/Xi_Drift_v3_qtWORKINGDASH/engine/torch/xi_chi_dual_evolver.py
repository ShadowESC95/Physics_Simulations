import torch

class XiChiDualEvolver:
    def __init__(self, shape=(64, 64), device=None, logger=None, rank=0):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.rank = rank
        self.logger = logger  # Accept external logger (or None)

        self.xi = torch.rand(shape, device=self.device)
        self.chi = torch.rand(shape, device=self.device)
        self.dt = 0.01
        self.kappa = 1.0
        self.coupling_strength = 0.3

    def evolve_step(self):
        lap_xi = self._laplacian(self.xi)
        lap_chi = self._laplacian(self.chi)
        interaction = self.coupling_strength * self.chi * self.xi

        self.xi = self.xi + self.dt * (lap_xi + interaction)
        self.chi = self.chi + self.dt * (lap_chi - interaction)

        # Optional inline logging
        if self.logger:
            entropy = torch.var(self.xi).item()
            xi_np, chi_np = self.get_numpy()
            self.logger.log_field_stats(xi_np, chi_np, entropy, step=None)  # You can supply step here if needed

    def _laplacian(self, field):
        return (
            -4 * field
            + torch.roll(field, 1, dims=0)
            + torch.roll(field, -1, dims=0)
            + torch.roll(field, 1, dims=1)
            + torch.roll(field, -1, dims=1)
        )

    def get_numpy(self):
        return self.xi.detach().cpu().numpy(), self.chi.detach().cpu().numpy()

    def photon_mass_squared(self):
        grad_x, grad_y = torch.gradient(self.xi)
        return self.kappa * (torch.norm(grad_x) ** 2 + torch.norm(grad_y) ** 2)
