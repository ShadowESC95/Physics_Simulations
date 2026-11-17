
from dolfinx import mesh, fem, io
from mpi4py import MPI
import numpy as np
import ufl
from petsc4py import PETSc

domain = mesh.create_unit_cube(MPI.COMM_WORLD, 32, 32, 32)
V = fem.FunctionSpace(domain, ("CG", 1))

u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)

Xi = fem.Function(V)
Xi.name = "Xi"
Chi = fem.Function(V)
Chi.name = "Chi"
Phi = fem.Function(V)
Phi.name = "Phi"

# Initial entropy distribution (Gaussian blob)
source_expr = lambda x: 10.0*np.exp(-100*((x[0]-0.5)**2 + (x[1]-0.5)**2 + (x[2]-0.5)**2))
f = fem.Function(V)
f.interpolate(source_expr)

dt = 0.01
T = 1.0
num_steps = int(T / dt)

# Weak form: ∂Ξ/∂t = ∇²Ξ + χ·Φ - decay
Xi_n = fem.Function(V)
Xi_n.interpolate(source_expr)

file = io.VTXWriter(domain.comm, "xi_chi_phi_evolution.pvd", [Xi, Chi, Phi], "xdmf")

for n in range(num_steps):
    Chi.interpolate(lambda x: np.sin(10*x[0]) * np.cos(10*x[1]))  # Example coherence modulation
    Phi.interpolate(lambda x: 0.1 + 0.05*np.sin(5*x[2]))  # Slow-varying coupling modulator

    a = u * v * ufl.dx + dt * ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
    L = (Xi_n + dt * Chi * Phi - dt * 0.01 * Xi_n) * v * ufl.dx

    problem = fem.petsc.LinearProblem(a, L, bcs=[], petsc_options={"ksp_type": "cg"})
    Xi_sol = problem.solve()
    Xi.x.array[:] = Xi_sol.x.array
    Xi_n.x.array[:] = Xi.x.array

    file.write(n * dt)

file.close()
