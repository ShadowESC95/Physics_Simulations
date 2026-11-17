from engine.torch.xi_evolver_torch import XiEvolver

xi_sim = XiEvolver()

for step in range(100):
    xi_sim.evolve_step()
    current_field = xi_sim.get_numpy()
    print(f"Step {step}: photon_mass² = {xi_sim.photon_mass_squared().item()}")
