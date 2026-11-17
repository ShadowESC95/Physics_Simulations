import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import meep as mp
import numpy as np
from modules.xi_chi_phi_modulator import generate_modulated_epsilon
from modules.nonlinear_kerr_module import apply_kerr_nonlinearity
from modules.spin_orbit_chiral import chiral_tensor_field
from modules.visualizer import save_h5_field

Nx, Ny, Nz = 64, 64, 64
resolution = 10
dpml = 1.0
t_max = 500
cell = mp.Vector3(Nx/resolution, Ny/resolution, Nz/resolution)
shape = (Nx, Ny, Nz)
eps_tensor = generate_modulated_epsilon(shape, time=0.0)
eps_tensor = apply_kerr_nonlinearity(eps_tensor, E_field=np.zeros((Nx, Ny, Nz, 3)))
eps_chiral = chiral_tensor_field(shape)
eps_scalar = np.mean(eps_tensor, axis=3)

geometry = [mp.Block(material=mp.Medium(epsilon=12.0),
                  size=mp.Vector3(Nx/resolution - 2*dpml,
                               Ny/resolution - 2*dpml,
                               Nz/resolution - 2*dpml))]

sources = [mp.Source(mp.GaussianSource(frequency=1.0, fwidth=0.3),
                  component=mp.Ez,
                  center=mp.Vector3(),
                  size=mp.Vector3())]

sim = mp.Simulation(cell_size=cell,
                 boundary_layers=[mp.PML(dpml)],
                 geometry=geometry,
                 sources=sources,
                 resolution=resolution)

sim.run(until=t_max)

Ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
Ez_data = np.reshape(Ez_data, (Nx, Ny, Nz))
os.makedirs("../outputs", exist_ok=True)
save_h5_field(Ez_data, "../outputs/E_field.h5")
