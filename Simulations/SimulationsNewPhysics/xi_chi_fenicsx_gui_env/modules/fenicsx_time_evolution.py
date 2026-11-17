#!/usr/bin/env python3
# Xi–Chi evolution with optional Poisson potential u
# Writes a single XDMF time series (recommended) and can also emit VTU/PVD.

from mpi4py import MPI
import numpy as np
import ufl
from dolfinx import mesh, fem, io
from dolfinx.fem.petsc import LinearProblem
from petsc4py import PETSc
import argparse, os, sys

# ------------------------- helpers -------------------------

def make_chi(V, mode: str, t: float = 0.0):
    """Construct Chi on space V according to 'mode'."""
    Chi = fem.Function(V); Chi.name = "Chi"
    if mode == "sincos":
        Chi.interpolate(lambda x: np.sin(6*x[0]) * np.cos(6*x[1]) * np.cos(4*x[2]))
    elif mode == "sincos_tv":   # time-varying example
        Chi.interpolate(lambda x: np.cos(2.0*np.pi*t) *
                                 np.sin(6*x[0]) * np.cos(6*x[1]) * np.cos(4*x[2]))
    elif mode == "gaussian":
        Chi.interpolate(lambda x: np.exp(-40.0*((x[0]-0.5)**2
                                              + (x[1]-0.5)**2
                                              + (x[2]-0.5)**2)))
    elif mode == "zero":
        Chi.x.array[:] = 0.0
    else:
        raise ValueError(f"Unknown --chi-mode '{mode}'")
    return Chi

def solve_poisson(V, rhs_fn, ksp_opts=None):
    """Solve -Δu = rhs_fn on the unit cube with homogeneous Neumann (natural) BCs."""
    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)
    a = ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
    L = rhs_fn * v * ufl.dx
    problem = LinearProblem(a, L, bcs=[], petsc_options=ksp_opts or {
        "ksp_type": "cg", "pc_type": "hypre", "ksp_rtol": 1e-8
    })
    sol = problem.solve()
    U = fem.Function(V); U.name = "u"
    U.x.array[:] = sol.x.array
    return U

def export_vtu_pvd_from_xdmf(xdmf_path, out_dir, pattern, start=0):
    """Robust VTU export + PVD builder (meshio first, VTK as fallback)."""
    os.makedirs(out_dir, exist_ok=True)
    wrote = 0
    try:
        import meshio
        with meshio.xdmf.TimeSeriesReader(xdmf_path) as rdr:
            pts, cells = rdr.read_points_cells()
            n = rdr.num_steps
            for k in range(n):
                _, pdat, cdat = rdr.read_data(k)
                meshio.Mesh(pts, cells, point_data=pdat, cell_data=cdat)\
                      .write(os.path.join(out_dir, pattern % (start + k)))
            wrote = n
    except Exception as e:
        print(f"[export] meshio failed, trying VTK/PyVista: {e}", file=sys.stderr)
        try:
            import pyvista as pv
            r = pv.get_reader(xdmf_path)
            times = getattr(r, "time_values", None) or []
            for k in range(len(times)):
                r.set_active_time_point(k)
                r.read().save(os.path.join(out_dir, pattern % (start + k)))
            wrote = len(times)
        except Exception as e2:
            print(f"[export] VTK also failed: {e2}", file=sys.stderr)
            return 0

    # PVD
    pvd = os.path.join(out_dir, os.path.splitext(os.path.basename(pattern))[0].split('%')[0] + "series.pvd")
    with open(pvd, "w") as f:
        f.write('<?xml version="1.0"?>\n<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n  <Collection>\n')
        for i in range(start, start + wrote):
            f.write(f'    <DataSet timestep="{i}" file="{pattern % i}"/>\n')
        f.write('  </Collection>\n</VTKFile>\n')
    print(f"[export] Wrote {wrote} VTU frame(s) to {out_dir} and {os.path.basename(pvd)}")
    return wrote

# ------------------------- main -------------------------

def main():
    ap = argparse.ArgumentParser(description="Xi–Chi time evolution (implicit Euler) + optional Poisson u")
    # mesh / FE
    ap.add_argument("--nx", type=int, default=32)
    ap.add_argument("--ny", type=int, default=32)
    ap.add_argument("--nz", type=int, default=32)
    ap.add_argument("--deg", type=int, default=1, help="CG polynomial degree")
    # time
    ap.add_argument("--steps", type=int, default=100)
    ap.add_argument("--dt", type=float, default=0.01)
    # PDE coefficients for Xi
    ap.add_argument("--kappa", type=float, default=1.0, help="diffusivity for Xi")
    ap.add_argument("--alpha", type=float, default=1.0, help="source coupling from Chi")
    ap.add_argument("--beta",  type=float, default=0.01, help="linear damping on Xi")
    # Chi / u choices
    ap.add_argument("--chi-mode", choices=["sincos", "sincos_tv", "gaussian", "zero"], default="sincos")
    ap.add_argument("--u-mode",   choices=["none", "poisson"], default="poisson")
    ap.add_argument("--u-rhs",    choices=["chi", "xi"], default="chi",
                    help="RHS for -Δu = rhs")
    # output
    ap.add_argument("--out", default="output/xi_chi_u_evolution.xdmf",
                    help="XDMF file to write")
    ap.add_argument("--emit-vtu", action="store_true",
                    help="Also export VTU frames + a PVD series at the end")
    ap.add_argument("--vtu-dir", default="output",
                    help="Directory for VTU/PVD (used with --emit-vtu)")
    ap.add_argument("--vtu-pattern", default="xi_chi_u_%04d.vtu",
                    help="Filename pattern for VTU frames (used with --emit-vtu)")
    args = ap.parse_args()

    comm = MPI.COMM_WORLD
    if comm.rank == 0:
        print(f"Solving on {args.nx}×{args.ny}×{args.nz}, steps={args.steps}, dt={args.dt}")
        print(f"PDE: dXi/dt = {args.kappa} ΔXi + {args.alpha} Chi - {args.beta} Xi")
        if args.u_mode == "poisson":
            print(f"u via Poisson: -Δu = {args.u_rhs}")

    # ----- mesh & space -----
    domain = mesh.create_unit_cube(comm, args.nx, args.ny, args.nz)
    V = fem.functionspace(domain, ("CG", args.deg))

    # Xi unknown & time level
    Xi   = fem.Function(V); Xi.name = "Xi"
    Xi_n = fem.Function(V); Xi_n.name = "Xi_n"
    Xi_n.interpolate(lambda x: 10.0*np.exp(-80.0*((x[0]-0.5)**2+(x[1]-0.5)**2+(x[2]-0.5)**2)))

    # trial/test for Xi step
    xi_trial = ufl.TrialFunction(V)
    v        = ufl.TestFunction(V)

    dt     = args.dt
    kappa  = args.kappa
    alpha  = args.alpha
    beta   = args.beta

    # implicit Euler for the diffusion part
    a_Xi = (xi_trial*v + dt*kappa*ufl.dot(ufl.grad(xi_trial), ufl.grad(v))) * ufl.dx

    # PETSc options once
    ksp_opts = {"ksp_type": "cg", "pc_type": "hypre", "ksp_rtol": 1e-8}

    # ensure output dir
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    # ----- time loop & output -----
    with io.XDMFFile(comm, args.out, "w") as xdmf:
        xdmf.write_mesh(domain)
        t = 0.0
        for n in range(args.steps):
            # Chi at this step
            Chi = make_chi(V, args.chi_mode, t);  Chi.name = "Chi"
            # explicit source/damping on Xi_n
            L_Xi = (Xi_n + dt*(alpha*Chi - beta*Xi_n)) * v * ufl.dx

            # solve Xi^{n+1}
            prob_Xi = LinearProblem(a_Xi, L_Xi, bcs=[], petsc_options=ksp_opts)
            Xi_sol  = prob_Xi.solve()
            Xi.x.array[:]   = Xi_sol.x.array
            Xi_n.x.array[:] = Xi.x.array

            # optional u each step
            if args.u_mode == "poisson":
                rhs = Chi if args.u_rhs == "chi" else Xi
                U = solve_poisson(V, rhs, ksp_opts)
            else:
                U = None

            t += dt
            # write *only* Xi, Chi, and optionally u, for this time t
            xdmf.write_function(Xi,  t)
            xdmf.write_function(Chi, t)
            if U is not None:
                xdmf.write_function(U, t)

    if comm.rank == 0:
        print(f"Wrote: {args.out}")
        if args.emit_vtu:
            export_vtu_pvd_from_xdmf(args.out, args.vtu_dir, args.vtu_pattern, start=0)

if __name__ == "__main__":
    main()

