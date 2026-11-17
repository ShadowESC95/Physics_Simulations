
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def compute_delta_theta(xi_field):
    grad_y, grad_x = np.gradient(xi_field)
    xi_safe = np.where(xi_field == 0, 1e-10, xi_field)
    grad_x_norm = grad_x / xi_safe
    return np.cumsum(grad_x_norm.mean(axis=0))  # along x-axis

def main():
    # Load your simulation field (placeholder path)
    xi = np.load('xi_sim_snapshot.npy')
    theta_model = compute_delta_theta(xi)

    # Load Planck-style birefringence curve (placeholder path)
    theta_planck = np.loadtxt('planck_biref_data.csv', delimiter=',')[:, 1]

    # Crop or interpolate to match lengths if necessary
    min_len = min(len(theta_model), len(theta_planck))
    theta_model = theta_model[:min_len]
    theta_planck = theta_planck[:min_len]

    # Correlation
    corr, _ = pearsonr(theta_model, theta_planck)
    print(f"Pearson correlation with Planck Δθ data: {corr:.4f}")

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(theta_model, label='Model Δθ(Ξ)')
    plt.plot(theta_planck, label='Planck Δθ(obs)', linestyle='--')
    plt.title("CMB Birefringence: Model vs. Planck")
    plt.xlabel("Pixel / Position")
    plt.ylabel("Δθ")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("birefringence_model_vs_planck.png")
    plt.show()

if __name__ == "__main__":
    main()
