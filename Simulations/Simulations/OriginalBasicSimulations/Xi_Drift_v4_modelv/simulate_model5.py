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
    drift_tensor_log = []

    for _ in range(steps):
        xi = rk4_step_model5(xi, chi, dt, lambda_coupling, gamma_5, m)
        xi_snapshots.append(xi.copy())

        # Normalized entropy
        flat = np.abs(xi.flatten())
        p = flat / np.sum(flat)
        p = p[p > 0]
        entropy = -np.sum(p * np.log(p))
        entropy_series.append(entropy)

        # G5 observable
        g5_series.append(np.mean(gamma_5 * xi**m))

        # Drift tensor (gradient squared)
        grad_x = np.gradient(xi, axis=0)
        grad_y = np.gradient(xi, axis=1)
        drift_tensor = grad_x**2 + grad_y**2
        drift_tensor_log.append(drift_tensor)

    # Convert logs to arrays
    xi_field_log = np.array(xi_snapshots)
    entropy_log = np.array(entropy_series)
    drift_tensor_log = np.array(drift_tensor_log)

    # Create output directory
    output_dir = f"model5_autosim_gamma{gamma_5}_m{m}"
    os.makedirs(output_dir, exist_ok=True)

    # Save logs for Dash or analysis
    np.save(os.path.join(output_dir, "xi_field_log.npy"), xi_field_log)
    np.save(os.path.join(output_dir, "entropy_log.npy"), entropy_log)
    np.save(os.path.join(output_dir, "drift_tensor_log.npy"), drift_tensor_log)

    # Save as text also for debugging or CSV plotting
    np.savetxt(os.path.join(output_dir, "entropy.csv"), entropy_log, delimiter=",")
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

