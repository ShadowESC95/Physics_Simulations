# in src/xichi/cli/run.py, add:
def thermo(cfg="config/sim.yaml"):
    import yaml
    from mpi4py import MPI
    from dolfinx import io
    from ..fenicsx.spaces import make_spaces
    from ..thermo.entropy_noether import entropy_fields, canonical_energy_chi, write_thermo_xdmf, reduce_violations
    with open(cfg,"r") as f: c=yaml.safe_load(f)
    comm = MPI.COMM_WORLD
    with io.XDMFFile(comm, c["output"]["path"], "r") as xf:
        domain = xf.read_mesh(name="Grid")
        Vscal, _ = make_spaces(domain, degree=c["mesh"]["degree"])
        Xi = fem.Function(Vscal); chi = fem.Function(Vscal)
        Xi_prev = fem.Function(Vscal); chi_prev = fem.Function(Vscal)
        try:
            while True:
                Xi_prev.x.array[:] = Xi.x.array[:]
                chi_prev.x.array[:] = chi.x.array[:]
                xf.read_function(Xi); xf.read_function(chi)
        except RuntimeError:
            pass
    s, sigma = entropy_fields(domain, Vscal, Xi, Xi_prev, c["time"]["dt"],
                              kappa=float(c["physics"].get("kappa",1.0)),
                              tau= float(c["physics"].get("tau", 0.0)),
                              c  = float(c["physics"]["c"]))
    e_chi = canonical_energy_chi(domain, Vscal, chi, chi_prev, c["time"]["dt"], float(c["physics"]["c"]))
    out_th = c["output"]["path"].replace(".xdmf","_thermo.xdmf")
    write_thermo_xdmf(out_th, domain, s, sigma, e_chi)
    gmin = reduce_violations(Vscal, sigma)
    if comm.rank==0:
        print(f"[xichi] thermo written -> {out_th}")
        if gmin < -1e-10:
            print(f"[xichi][SECOND-LAW WARNING] min entropy production = {gmin:.3e} < 0 (check dt, tau, kappa).")
        else:
            print(f"[xichi] entropy production non-negative within tolerance (min {gmin:.3e}).")
