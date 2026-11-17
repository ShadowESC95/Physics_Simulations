# solver/xi_chi_solver.py
import numpy as np
from mpi4py import MPI
import dolfinx
from dolfinx import fem, mesh
from petsc4py import PETSc

# Physical constants and coupling (using calibration to Maxwell)
ε0 = 8.854e-12  # vacuum permittivity (F/m)
μ0 = 4e-7*np.pi  # vacuum permeability (N/A^2)
c = 1.0/np.sqrt(μ0*ε0)  # speed of light
# Coupling parameters (choose alpha+delta=0, gamma=1/ε0 for wave equations:contentReference[oaicite:13]{index=13})
alpha = 1.0
delta = -1.0  # so alpha + delta = 0
gamma = 1.0/ε0
kappa = 1.0   # (choose kappa=1 for now; can be adjusted)

# Create computational mesh (e.g., unit cube with given resolution)
L = 1.0
Nx = Ny = Nz = 50  # mesh resolution
domain = mesh.create_box(MPI.COMM_WORLD,
                         [[0.0, 0.0, 0.0], [L, L, L]],
                         [Nx, Ny, Nz],
                         cell_type=mesh.CellType.tetrahedron)

# Define function space for scalar fields (CG1)
V = fem.FunctionSpace(domain, ("CG", 1))

# Define trial and test functions for Ξ and χ (we solve as a system or sequentially)
Xi = fem.Function(V)            # Ξ at current time
Xi_old = fem.Function(V)        # Ξ at previous time (for time stepping)
Xi_new = fem.Function(V)        # Ξ at next time (solution unknown)
Chi = fem.Function(V)           # χ at current time
Chi_old = fem.Function(V)       # χ at previous time
Chi_new = fem.Function(V)       # χ at next time

# Initialize fields (using our initialization module)
from initialization import field_init
field_init.initialize_fields(Xi, Chi)

# Set up variational forms for wave equations: Ξ_tt = c^2 ∇^2 Ξ + source_Ξ, and similarly for χ.
# We implement a second-order time-step manually (leap-frog / central differences).
dt = 1e-3  # time step
# For simplicity, store also first time-derivatives if needed
Xi_dot = fem.Function(V)   # dΞ/dt
Chi_dot = fem.Function(V)  # dχ/dt

# Define source terms (e.g., charge density ρ and current J distributions)
# For demonstration: a point charge at center for Ξ, and no explicit source for χ initially.
x = V.tabulate_dof_coordinates()  # coordinates of degrees of freedom
x0 = np.array([L/2, L/2, L/2])
rho0 = 1.0  # some charge magnitude
# Set source for Ξ as -rho/(gamma*ε0) (Poisson source) if static, or time-varying if desired
rho = rho0 * np.exp(-np.linalg.norm(x - x0, axis=1)**2 / (0.1**2))
# (We embed rho in the equation via a forcing term below)

# Define trial/test (for variational form, though using explicit scheme we might not need solve a linear system)
u = fem.Function(V)   # dummy trial
v = fem.TestFunction(V)

# Assemble Laplacian operator (stiffness matrix) for Δ (∇^2) using variational form:
u_trial = fem.TrialFunction(V)
a_laplace = fem.form(fem.dot(fem.grad(u_trial), fem.grad(v)) * fem.dx)
A_laplace = fem.petsc.assemble_matrix(a_laplace, [])
A_laplace.assemble()
# Convert to PETSc matrix (already PETSc via dolfinx) and factor if needed for implicit solve
# (For explicit, we'll use matrix-vector application)

# Time-stepping loop
t = 0.0
T_end = 1.0  # end time
output_interval = 0.01
frame = 0
# Pre-compute source term in Ξ-equation: f_Xi = -(rho/(gamma*ε0)) (from ∇²Ξ = -ρ/(γ ε0):contentReference[oaicite:14]{index=14})
# We'll incorporate this in time stepping for Xi.
f_Xi = rho / (gamma*ε0)
# (No explicit source for χ in this simple scenario; χ may be excited through coupling if implemented)

# Initialize Xi_old, Chi_old (at t=0-dt) by a backward step or assume initial velocity 0
Xi_old.x.array[:] = Xi.x.array[:]  # for first step, assume no change (static start)
Chi_old.x.array[:] = Chi.x.array[:]

# Main loop
while t < T_end + 1e-9:
    # Compute Laplacian of current fields (A_laplace * field vector)
    lap_Xi = A_laplace.mult(Xi.vector.copy())   # ΔΞ
    lap_Chi = A_laplace.mult(Chi.vector.copy()) # Δχ

    # Explicit central difference update for wave eq: Xi_new = 2*Xi - Xi_old + (c*dt)^2 * ΔΞ + dt^2 * source
    Xi_new.x.array[:] = (2.0 * Xi.x.array - Xi_old.x.array
                         + (c*dt)**2 * lap_Xi.array
                         - (dt**2) * f_Xi)              # note: subtract because equation is Ξ_tt = c^2 ∇²Ξ + ... -> ΔΞ appears with + sign
    Chi_new.x.array[:] = (2.0 * Chi.x.array - Chi_old.x.array
                          + (c*dt)**2 * lap_Chi.array)
    # (Above, we set source for χ as 0; coupling terms could be added here if needed)

    # Update time derivative estimates (if needed for observables or future use)
    Xi_dot.x.array[:] = (Xi_new.x.array - Xi_old.x.array) / (2*dt)
    Chi_dot.x.array[:] = (Chi_new.x.array - Chi_old.x.array) / (2*dt)

    # Shift time frames for next step
    Xi_old.x.array[:] = Xi.x.array[:]
    Xi.x.array[:]     = Xi_new.x.array[:]
    Chi_old.x.array[:] = Chi.x.array[:]
    Chi.x.array[:]     = Chi_new.x.array[:]

    t += dt

    # Output results periodically
    if t >= frame * output_interval:
        # Save Ξ and χ to XDMF/H5 file for visualization
        with dolfinx.io.XDMFFile(MPI.COMM_WORLD, f"data/fields_{frame:04d}.xdmf", "w") as xdmf:
            xdmf.write_mesh(domain)
            xdmf.write_function(Xi, t)
            xdmf.write_function(Chi, t)
        frame += 1

# After loop, ensure final data is saved

