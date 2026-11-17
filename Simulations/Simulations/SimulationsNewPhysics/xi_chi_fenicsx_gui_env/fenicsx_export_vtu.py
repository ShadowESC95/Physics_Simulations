
from dolfinx import mesh, fem, io
import ufl
import numpy as np
import pyvista as pv
from mpi4py import MPI
from petsc4py import PETSc

domain = mesh.create_unit_cube(MPI.COMM_WORLD, 32, 32, 32)
V = fem.FunctionSpace(domain, ("CG", 1))

u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)

Xi = fem.Function(V)
Xi.name = "Xi"

f_expr = fem.Expression("10.0*exp(-100*((x[0]-0.5)*(x[0]-0.5)+(x[1]-0.5)*(x[1]-0.5)+(x[2]-0.5)*(x[2]-0.5)))", V.element.interpolation_points())
f = fem.Function(V)
f.interpolate(lambda x: 10.0*np.exp(-100*((x[0]-0.5)**2 + (x[1]-0.5)**2 + (x[2]-0.5)**2)))

a = ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = f * v * ufl.dx

problem = fem.petsc.LinearProblem(a, L, bcs=[], petsc_options={"ksp_type": "cg"})
Xi = problem.solve()

# Export to VTU file for visualization
with io.VTXWriter(domain.comm, "xi_field000.vtu", [Xi], "xdmf") as vtx:
    vtx.write(0.0)
