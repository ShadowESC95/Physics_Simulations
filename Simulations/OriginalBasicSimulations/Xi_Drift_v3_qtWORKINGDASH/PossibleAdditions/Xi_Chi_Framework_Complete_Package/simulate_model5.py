
import numpy as np
import os
import argparse

def laplacian(field):
    return np.gradient(np.gradient(field, axis=0), axis=0) + np.gradient(np.gradient(field, axis=1), axis=1)

def rk4_step_model5(xi, chi, dt, lambda_coupling, gamma_5, m):
    def rhs(xi, chi):
        lap_xi = laplacian(xi)
        lap_chi = laplacian(chi)
        G5 = gamma_5 * xi**m
        return lap_xi + lambda_coupling * xi * chi + G5 * lap_chi

    k1 = rhs(xi, chi)
    k2 = rhs(xi + 0.5 * dt * k1, chi)
    k3 = rhs(xi + 0.5 * dt * k2, chi)
    k4 = rhs(xi + dt * k3, chi)
    return xi + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def main(steps, gamma_5, m, lambda_coupling, dt):
    size = 100
    xi = np.random.normal(0.5, 0.1, (size, size))
    chi = np.random.normal(0.0, 0.01, (size, size))

    xi_snapshots = []
    entropy_series = []
    g5_series = []

    for _ in range(steps):
        xi = rk4_step_model5(xi, chi, dt, lambda_coupling, gamma_5, m)
        xi_snapshots.append(xi.copy())
        p = np.abs(xi.flatten()) / np.sum(np.abs(xi.flatten()))
        p = p[p > 0]
        entropy_series.append(-np.sum(p * np.log(p)))
        g5_series.append(np.mean(gamma_5 * xi**m))

    output_dir = f"model5_autosim_gamma{gamma_5}_m{m}"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, xi_snap in enumerate(xi_snapshots):
        np.save(os.path.join(output_dir, f"xi_snapshot_{i:03d}.npy"), xi_snap)
    
    np.savetxt(os.path.join(output_dir, "entropy.csv"), entropy_series, delimiter=",")
    np.savetxt(os.path.join(output_dir, "g5_series.csv"), g5_series, delimiter=",")
    print(f"Simulation complete. Data saved to {output_dir}/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--gamma_5", type=float, default=0.05)
    parser.add_argument("--m", type=float, default=1.0)
    parser.add_argument("--lambda_coupling", type=float, default=0.3)
    parser.add_argument("--dt", type=float, default=0.01)
    args = parser.parse_args()

    main(args.steps, args.gamma_5, args.m, args.lambda_coupling, args.dt)
