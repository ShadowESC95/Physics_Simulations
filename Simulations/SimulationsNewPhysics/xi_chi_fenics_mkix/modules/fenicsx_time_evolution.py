
from mpi4py import MPI
import numpy as np, ufl, argparse
from dolfinx import mesh, fem, io
from dolfinx.fem.petsc import LinearProblem

def gaussian3d(x, A=10.0, s=80.0):
    return A*np.exp(-s*((x[0]-0.5)**2+(x[1]-0.5)**2+(x[2]-0.5)**2))

def chi_field(x, mode="sincos"):
    if mode == "sincos":
        return np.sin(6*x[0])*np.cos(6*x[1])*np.cos(4*x[2])
    if mode == "gaussian":
        return gaussian3d(x, A=1.0, s=60.0)
    return 0.0

def solve_poisson(V, rhs_fun):
    u = ufl.TrialFunction(V); v = ufl.TestFunction(V)
    a = ufl.dot(ufl.grad(u), ufl.grad(v))*ufl.dx
    L = rhs_fun*v*ufl.dx
    prob = LinearProblem(a, L, bcs=[], petsc_options={"ksp_type":"cg","pc_type":"hypre","ksp_rtol":1e-8})
    uh = prob.solve(); uh.name="u"; return uh

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nx", type=int, default=32); ap.add_argument("--ny", type=int, default=32); ap.add_argument("--nz", type=int, default=32)
    ap.add_argument("--steps", type=int, default=100); ap.add_argument("--dt", type=float, default=0.01); ap.add_argument("--deg", type=int, default=1)
    ap.add_argument("--kappa", type=float, default=1.0); ap.add_argument("--alpha", type=float, default=1.0); ap.add_argument("--beta", type=float, default=0.01)
    ap.add_argument("--chi-mode", default="sincos", choices=["sincos","gaussian","const0"])
    ap.add_argument("--u-mode", default="none", choices=["none","poisson"]); ap.add_argument("--u-rhs", default="chi", choices=["chi","xi","laplace_xi"])
    ap.add_argument("--out", default="data/output/xi_chi_u_evolution.xdmf")
    args = ap.parse_args()

    comm = MPI.COMM_WORLD
    domain = mesh.create_unit_cube(comm, args.nx, args.ny, args.nz)
    V = fem.functionspace(domain, ("CG", args.deg))
    Xi, Chi = fem.Function(V), fem.Function(V)
    Xi.name="Xi"; Chi.name="Chi"
    Xi_n = fem.Function(V); Xi_n.name="Xi_n"
    Xi_n.interpolate(lambda x: gaussian3d(x))
    if args.chi_mode=="const0":
        Chi.x.array[:] = 0.0
    else:
        Chi.interpolate(lambda x: chi_field(x, mode=args.chi_mode))

    dt=args.dt; u,v = ufl.TrialFunction(V), ufl.TestFunction(V)
    a = (u*v + dt*args.kappa*ufl.dot(ufl.grad(u), ufl.grad(v)))*ufl.dx

    with io.XDMFFile(comm, args.out, "w") as xdmf:
        xdmf.write_mesh(domain)
        t=0.0
        for _ in range(args.steps):
            if args.chi_mode=="sincos":
                Chi.interpolate(lambda x: chi_field(x, "sincos"))
            L = (Xi_n + dt*args.alpha*Chi - dt*args.beta*Xi_n) * v * ufl.dx
            Xi_sol = LinearProblem(a, L, petsc_options={"ksp_type":"cg","pc_type":"hypre","ksp_rtol":1e-8}).solve()
            Xi.x.array[:] = Xi_sol.x.array

            uh=None
            if args.u_mode=="poisson":
                if args.u_rhs=="chi":
                    rhs=Chi
                elif args.u_rhs=="xi":
                    rhs=Xi
                else:
                    rt, vv = ufl.TrialFunction(V), ufl.TestFunction(V)
                    aP = rt*vv*ufl.dx; LP = -ufl.dot(ufl.grad(Xi), ufl.grad(vv))*ufl.dx
                    rhs_tmp = LinearProblem(aP, LP, petsc_options={"ksp_type":"cg","pc_type":"hypre","ksp_rtol":1e-8}).solve()
                    rhs = rhs_tmp
                uh = solve_poisson(V, rhs)

            Xi_n.x.array[:] = Xi.x.array; t += dt
            xdmf.write_function(Xi, t); xdmf.write_function(Chi, t)
            if uh is not None: xdmf.write_function(uh, t)

    if comm.rank==0:
        print("Wrote:", args.out)

if __name__=="__main__":
    main()
