
import os, json, csv
import numpy as np
import matplotlib.pyplot as plt
from solver_1p1d import run_sim
from analysis import phase_velocity_avg

OUTDIR = os.path.join(os.path.dirname(__file__), "out_sweep")
os.makedirs(OUTDIR, exist_ok=True)

def main():
    with open("config.json","r") as f:
        base = json.load(f)

    epsilons = np.logspace(-6, -3, 10)
    rows = []
    for e in epsilons:
        params = json.loads(json.dumps(base))
        params['epsilon_s'] = float(e)
        x, final, energies = run_sim(params)
        vph = phase_velocity_avg(final['Xi'], final['chi'], params)
        rows.append(dict(epsilon_s=e, energy_final=float(energies[-1]), v_phase=float(vph),
                         Xi_mean=float(final['Xi'].mean()), chi_mean=float(final['chi'].mean())))

    csv_path = os.path.join(OUTDIR,'epsilon_sweep.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)

    eps = [r['epsilon_s'] for r in rows]
    plt.figure(); plt.loglog(eps, [r['v_phase'] for r in rows], marker='o')
    plt.xlabel('epsilon_s (Stueckelberg coupling)'); plt.ylabel('phase velocity (avg)')
    plt.title('Phase velocity vs epsilon_s')
    plt.tight_layout(); plt.savefig(os.path.join(OUTDIR,'vphase_vs_eps.png'), dpi=160); plt.close()

    plt.figure(); plt.semilogx(eps, [r['energy_final'] for r in rows], marker='o')
    plt.xlabel('epsilon_s'); plt.ylabel('<Energy> final')
    plt.title('Final energy vs epsilon_s')
    plt.tight_layout(); plt.savefig(os.path.join(OUTDIR,'energy_vs_eps.png'), dpi=160); plt.close()

if __name__ == "__main__":
    main()
