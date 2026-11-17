
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.xi_chi_phi_modulator import generate_modulated_epsilon
import meep as mp
import numpy as np
from modules.xi_chi_phi_modulator import generate_modulated_epsilon
from modules.nonlinear_kerr_module import apply_kerr_nonlinearity
from modules.spin_orbit_chiral import chiral_tensor_field
from modules.visualizer import save_h5_field
from meep.geom import Vector3

Nx, Ny, Nz = 128, 128, 128
resolution = 20
cell = Vector3(Nx/resolution, Ny/resolution, Nz/resolution)
t_max = 5000 / resolution
dpml = 1.0

shape = (Nx, Ny, Nz)
epsilon_mod = generate_modulated_epsilon(shape, time=0.0)
epsilon_mod = apply_kerr_nonlinearity(epsilon_mod, E_field=np.zeros((Nx, Ny, Nz, 3)))
epsilon_chiral = chiral_tensor_field(shape)
eps_scalar = np.mean(epsilon_mod, axis=(3))

geometry = [mp.Block(material=mp.Medium(epsilon=12.0),
                     size=Vector3(Nx/resolution - 2*dpml,
                                     Ny/resolution - 2*dpml,
                                     Nz/resolution - 2*dpml))]

sources = [mp.Source(mp.GaussianSource(frequency=1.0, fwidth=0.4),
                     component=mp.Ez,
                     center=mp.Vector3(),
                     size=mp.Vector3())]

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=[mp.PML(dpml)],
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution,
                    default_material=mp.Medium(epsilon=12.0))

sim.run(until=t_max)

E_field = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
E_field = np.reshape(E_field, (Nx, Ny, Nz))
os.makedirs("../outputs", exist_ok=True)
save_h5_field(E_field, "../outputs/E_field.h5")


