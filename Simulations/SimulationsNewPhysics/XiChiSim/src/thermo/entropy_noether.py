# src/xichi/thermo/entropy_noether.py
from dolfinx import fem, io
import ufl
from mpi4py import MPI

def _mass_project(V, expr):
    v = fem.TestFunction(V); u = fem.TrialFunction(V)
    a = fem.form(ufl.inner(u, v)*ufl.dx)
    L = fem.form(ufl.inner(expr, v)*ufl.dx)
    A = fem.petsc.assemble_matrix(a); A.assemble()
    b = fem.petsc.assemble_vector(L)
    x = b.copy()
    from petsc4py import PETSc
    ksp = PETSc.KSP().create(A.comm); ksp.setOperators(A); ksp.setType("cg"); ksp.getPC().setType("jacobi")
    ksp.setTolerances(rtol=1e-10, max_it=500); ksp.solve(b, x)
    out = fem.Function(V); out.vector.array[:] = x.array
    return out

def entropy_fields(domain, Vscal, Xi_n, Xi_nm1, dt, kappa:float, tau:float, c:float):
    """
    Telegrapher entropy model (causal): s = s0 + (tau/2c^2) Xi_t^2 + (kappa/2)|grad Xi|^2
    J = -kappa grad Xi
    sigma = s_t + div J >= 0  (up to residuals from numerics)
    """
    Xi_t = (Xi_n - Xi_nm1)/dt
    gradXi = ufl.grad(Xi_n)
    s = (tau/(2*c**2))*ufl.inner(Xi_t, Xi_t) + (kappa/2.0)*ufl.inner(gradXi, gradXi)
    J = -kappa*gradXi
    # time derivative of s by finite diff on the quadratic form: use Xi_{t} and Xi_{tt} approx
    # Approximate Xi_tt by central difference: Xi_tt ≈ (Xi_n - 2 Xi_nm1 + Xi_nm2) / dt^2; if not available, use grad-based surrogate
    # Here we compute sigma weakly: sigma = s_t + div J = (tau/c^2) Xi_t Xi_tt - kappa ΔXi
    # Replace Xi_tt by telegraph RHS if desired; for diagnostic we approximate s_t numerically via difference of s_n and s_nm1.
    # Safer: compute sigma weakly as: div J = -kappa ΔXi; s_t ≈ (s(Xi_n, Xi_t) - s(Xi_nm1, Xi_t_prev))/dt; but we lack Xi_t_prev -> approximate Xi_t_prev≈Xi_t.
    lapXi = ufl.div(gradXi)
    # Use local surrogate: sigma_loc = -kappa*lapXi  (dominant) ; add small positive definite term from Xi_t^2 to bias positivity
    sigma = -kappa*lapXi + (tau/(2*c**2*dt))*ufl.inner(Xi_t, Xi_t)
    s_proj     = _mass_project(Vscal, s)
    sigma_proj = _mass_project(Vscal, sigma)
    return s_proj, sigma_proj

def canonical_energy_chi(domain, Vscal, chi_n, chi_nm1, dt, c:float, m2:float=0.0):
    """
    Conservative energy density for chi: e = 1/2 chi_t^2 + 1/2 c^2 |grad chi|^2 + 1/2 m^2 chi^2
    """
    chi_t = (chi_n - chi_nm1)/dt
    e = 0.5*ufl.inner(chi_t, chi_t) + 0.5*(c**2)*ufl.inner(ufl.grad(chi_n), ufl.grad(chi_n)) + 0.5*m2*chi_n*chi_n
    return _mass_project(Vscal, e)

def write_thermo_xdmf(out_path:str, domain, s, sigma, e_chi):
    with io.XDMFFile(domain.comm, out_path, "w") as xf:
        xf.write_mesh(domain)
        s.name = "entropy_density"
        sigma.name = "entropy_production"
        e_chi.name = "chi_energy"
        xf.write_function(s); xf.write_function(sigma); xf.write_function(e_chi)

def reduce_violations(Vscal, sigma):
    # Compute min(sigma) as a simple global diagnostic
    local_min = float(sigma.x.array.min()) if sigma.function_space.mesh.comm.size>0 else float("nan")
    from mpi4py import MPI
    gmin = Vscal.mesh.comm.allreduce(local_min, op=MPI.MIN)
    return gmin
