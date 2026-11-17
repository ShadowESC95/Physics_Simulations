#!/usr/bin/env python3
import argparse
from pathlib import Path
import numpy as np

from mpi4py import MPI
from dolfinx import fem, mesh, default_scalar_type
from dolfinx.fem.petsc import LinearProblem
from dolfinx.io import XDMFFile
import ufl

comm = MPI.COMM_WORLD
rank = comm.rank

def FS(msh, element=("Lagrange", 1)):
    # 0.9 uses fem.functionspace; older used fem.FunctionSpace
    try:
        return fem.functionspace(msh, element)
    except AttributeError:
        return fem.FunctionSpace(msh, element)

def solve_poisson(nx=24, ny=24, nz=24):
    """∇²u = 1 on [0,1]^3 with u=0 on x=0 and x=1."""
    msh = mesh.create_unit_cube(comm, nx, ny, nz, cell_type=mesh.CellType.tetrahedron)
    V = FS(msh, ("Lagrange", 1))

    u = fem.Function(V)
    u_trial = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)

    # ✅ correct scalar type for dolfinx 0.9
    f = fem.Constant(msh, default_scalar_type(1.0))

    # Dirichlet BC on x=0 and x=1
    def on_x0(x): return np.isclose(x[0], 0.0)
    def on_x1(x): return np.isclose(x[0], 1.0)
    uD = fem.Function(V); uD.x.array[:] = 0.0
    bcs = [
        fem.dirichletbc(uD, fem.locate_dofs_geometrical(V, on_x0)),
        fem.dirichletbc(uD, fem.locate_dofs_geometrical(V, on_x1)),
    ]

    a = fem.form(ufl.inner(ufl.grad(u_trial), ufl.grad(v)) * ufl.dx)
    L = fem.form(f * v * ufl.dx)

    # ✅ do NOT pass petsc_options (let CLI options be used)
    problem = LinearProblem(a, L, bcs=bcs, u=u)
    uh = problem.solve()
    try:
        uh.name = "u"
    except Exception:
        pass
    return msh, V, uh

def write_xdmf(msh, uh, outdir: Path, stem="poisson3d_u"):
    outdir.mkdir(parents=True, exist_ok=True)
    with XDMFFile(comm, str(outdir / f"{stem}.xdmf"), "w") as xdmf:
        xdmf.write_mesh(msh)
        xdmf.write_function(uh)
    if rank == 0:
        print(f"[xdmf]   → {outdir / (stem + '.xdmf')}")




def write_vtu(msh, V, uh, outdir: Path, stem="poisson3d_u"):
    """Convert the first step of the XDMF (grid collection) to a VTU using meshio's TimeSeriesReader."""
    try:
        import meshio
        xdmf = outdir / f"{stem}.xdmf"
        if not xdmf.exists():
            if rank == 0:
                print(f"[vtu] missing {xdmf}; nothing to convert")
            return

        with meshio.xdmf.TimeSeriesReader(str(xdmf)) as r:
            points, cells = r.read_points_cells()
            # grab first step (k=0)
            t, point_data, cell_data = r.read_data(0)

        # ensure we have a scalar named 'Xi' for the viewer
        pd = dict(point_data or {})
        if "Xi" not in pd:
            # prefer 'u' if present
            if "u" in pd:
                pd["Xi"] = pd["u"]
            elif len(pd) == 1:
                # single field; alias it
                only = next(iter(pd))
                pd["Xi"] = pd[only]

        out = outdir / f"{stem}_0000.vtu"
        meshio.write_points_cells(
            str(out),
            points,
            cells,            # list of (cell_type, ndarray)
            point_data=pd,
            cell_data=cell_data or None,
        )
        if rank == 0:
            print(f"[vtu]    → {out}  (point_data={list(pd.keys())})")
    except Exception as e:
        if rank == 0:
            print(f"[vtu] failed: {e}")


def main():
    ap = argparse.ArgumentParser(description="Poisson 3D (dolfinx 0.7–0.9)")
    ap.add_argument("--nx", type=int, default=24)
    ap.add_argument("--ny", type=int, default=24)
    ap.add_argument("--nz", type=int, default=24)
    ap.add_argument("--out", type=Path, default=Path("output"))
    ap.add_argument("--stem", type=str, default="poisson3d_u")
    ap.add_argument("--write-vtu", action="store_true")
    args, _ = ap.parse_known_args()

    if rank == 0:
        print(f"Solving on {args.nx}×{args.ny}×{args.nz} tets…")

    msh, V, uh = solve_poisson(args.nx, args.ny, args.nz)
    write_xdmf(msh, uh, args.out, stem=args.stem)
    if args.write_vtu:
        write_vtu(msh, V, uh, args.out, stem=args.stem)

if __name__ == "__main__":
    main()
