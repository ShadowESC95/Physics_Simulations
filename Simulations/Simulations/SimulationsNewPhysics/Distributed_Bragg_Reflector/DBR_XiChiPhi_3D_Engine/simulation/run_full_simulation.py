
import meep as mp
import numpy as np
import h5py
from modules.xi_chi_phi_modulator import generate_modulated_epsilon
from modules.nonlinear_kerr_module import apply_kerr_nonlinearity
from modules.spin_orbit_chiral import chiral_tensor_field
from modules.visualizer import save_h5_field

# Grid and time configuration
Nx, Ny, Nz = 128, 128, 128
resolution = 20
cell = mp.Vector3(Nx/resolution, Ny/resolution, Nz/resolution)
t_max = 5000 / resolution
dpml = 1.0

# Permittivity setup
shape = (Nx, Ny, Nz)
epsilon_mod = generate_modulated_epsilon(shape, time=0.0)
epsilon_mod = apply_kerr_nonlinearity(epsilon_mod, E_field=np.zeros((Nx, Ny, Nz, 3)))
epsilon_chiral = chiral_tensor_field(shape)

# Combine permittivity (simplified scalar field for Meep)
eps_scalar = np.mean(epsilon_mod, axis=(3))  # take average across polarization

# Geometry using medium modulator
geometry = [mp.Block(material=mp.Medium(epsilon=12.0),
                     size=mp.Vector3(Nx/resolution - 2*dpml,
                                     Ny/resolution - 2*dpml,
                                     Nz/resolution - 2*dpml))]

# Source: broadband Gaussian pulse
sources = [mp.Source(mp.GaussianSource(frequency=1.0, fwidth=0.4),
                     component=mp.Ez,
                     center=mp.Vector3(),
                     size=mp.Vector3())]

# Simulation
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=[mp.PML(dpml)],
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution,
                    default_material=mp.Medium(epsilon=12.0))

# Run simulation
sim.run(until=t_max)

# Extract and save E-field
E_field = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
E_field = np.reshape(E_field, (Nx, Ny, Nz))
save_h5_field(E_field, "outputs/E_field.h5")
