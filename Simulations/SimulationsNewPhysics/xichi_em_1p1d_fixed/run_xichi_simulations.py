
import json, os
import numpy as np
import matplotlib.pyplot as plt
from solver_1p1d import run_sim
from analysis import phase_velocity_avg, track_pulse_speed

OUTDIR = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUTDIR, exist_ok=True)

def main():
    with open("config.json","r") as f:
        params = json.load(f)

    snapshots = {}
    def cb(n, x, state, H):
        snapshots[n] = (x, {k:v.copy() for k,v in state.items()}, H.copy())

    x, final, energies = run_sim(params, out_callback=cb)

    dt = params['dt']; steps = params['steps']
    times = np.arange(0, steps+1)*dt

    plt.figure(figsize=(10,6))
    for fld in ['Xi','chi','AE','AB']:
        plt.plot(x, final[fld], label=fld)
    plt.legend(); plt.xlabel("x"); plt.ylabel("field"); plt.title("Final fields")
    plt.tight_layout(); plt.savefig(os.path.join(OUTDIR,'final_fields.png'), dpi=160); plt.close()

    plt.figure()
    plt.plot(times[:len(energies)], energies)
    plt.xlabel("time"); plt.ylabel("<Energy density>"); plt.title("Energy evolution")
    plt.tight_layout(); plt.savefig(os.path.join(OUTDIR,'energy_evolution.png'), dpi=160); plt.close()

    vph = phase_velocity_avg(final['Xi'], final['chi'], params)
    with open(os.path.join(OUTDIR,'observables.txt'),'w') as f:
        f.write(f"phase_velocity_avg ~ {vph:.6g}\n")

    keys = sorted(k for k in snapshots.keys())
    if len(keys) >= 2:
        k0, k1 = keys[0], keys[min(5, len(keys)-1)]
        x0, s0, _ = snapshots[k0]
        x1, s1, _ = snapshots[k1]
        vg = track_pulse_speed(x0, s0['AE'], s1['AE'], (k1-k0)*dt)
        with open(os.path.join(OUTDIR,'observables.txt'),'a') as f:
            f.write(f"group_velocity_est ~ {vg:.6g}\n")

if __name__ == "__main__":
    main()
