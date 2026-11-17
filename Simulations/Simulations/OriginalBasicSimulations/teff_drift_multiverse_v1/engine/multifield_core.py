import torch

def run_multifield_simulation(steps, grid_size, dt, device="cpu", coupling_strength=0.05):
    phi1 = torch.ones((grid_size, grid_size), device=device)
    phi2 = torch.ones((grid_size, grid_size), device=device)

    phi1 += 0.01 * torch.randn_like(phi1)
    phi2 += 0.01 * torch.randn_like(phi2)

    log_phi1, log_phi2 = [], []

    for step in range(steps):
        lap1 = -4 * phi1 + torch.roll(phi1, 1, 0) + torch.roll(phi1, -1, 0) + \
                        torch.roll(phi1, 1, 1) + torch.roll(phi1, -1, 1)
        lap2 = -4 * phi2 + torch.roll(phi2, 1, 0) + torch.roll(phi2, -1, 0) + \
                        torch.roll(phi2, 1, 1) + torch.roll(phi2, -1, 1)

        dphi1 = lap1 - phi1 * (phi1 - 1)**2 + coupling_strength * (phi2 - phi1)
        dphi2 = lap2 - phi2 * (phi2 - 1)**2 + coupling_strength * (phi1 - phi2)

        phi1 += dt * dphi1
        phi2 += dt * dphi2

        if step % 5 == 0:
            log_phi1.append(phi1.detach().cpu().numpy())
            log_phi2.append(phi2.detach().cpu().numpy())

    return log_phi1, log_phi2
