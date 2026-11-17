
from dolfinx import mesh, fem, io
from mpi4py import MPI
import numpy as np
import ufl
import pyvista as pv
from petsc4py import PETSc

domain = mesh.create_unit_cube(MPI.COMM_WORLD, 32, 32, 32)
V = fem.FunctionSpace(domain, ("CG", 1))


u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)

Xi = fem.Function(V)
Xi.name = "Xi"

# Entropic Gaussian seed
f = fem.Function(V)
f.interpolate(lambda x: 10.0*np.exp(-100*((x[0]-0.5)**2 + (x[1]-0.5)**2 + (x[2]-0.5)**2)))

a = ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = f * v * ufl.dx

problem = fem.petsc.LinearProblem(a, L, bcs=[], petsc_options={"ksp_type": "cg"})
Xi = problem.solve()

# Live stream to ParaView Catalyst output directory
with io.VTXWriter(domain.comm, "live_xi_stream.pvd", [Xi], "xdmf") as vtx:
    vtx.write(0.0)
