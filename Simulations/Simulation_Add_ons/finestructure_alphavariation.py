import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Generate a synthetic final Ξ field ---
np.random.seed(0)
xi_final = np.random.randn(32, 32) * 0.1 + 1.0  # Example: small random fluctuation around 1

# Simulate fine-structure constant α drift over final Ξ field: α(Ξ) = α₀ (Ξ₀ / Ξ)^δ
alpha_0 = 1/137
xi_0 = np.mean(xi_final)
delta = 0.02  # small drift sensitivity exponent

# Compute α field
alpha_field = alpha_0 * (xi_0 / xi_final) ** delta
alpha_mean = np.mean(alpha_field)
alpha_std = np.std(alpha_field)

# Generate synthetic absorption "spectrum"
# Assume transitions sensitive to α^2, plot peak shift ∝ α
wavelengths = np.linspace(120, 130, xi_final.shape[1])  # in nm
spectrum_base = np.exp(-((wavelengths - 125) ** 2) / (2 * 0.5 ** 2))  # baseline absorption profile

# α variation shifts the central wavelength by a small factor
shifts = (alpha_field.mean(axis=0) / alpha_0 - 1) * 125  # nm shift
shifted_spectra = np.array([
    np.exp(-((wavelengths - (125 + shift)) ** 2) / (2 * 0.5 ** 2)) for shift in shifts
])

# Average synthetic spectrum
synthetic_spectrum = shifted_spectra.mean(axis=0)

# Save alpha variation
df_alpha = pd.DataFrame({
    "x_position": np.arange(alpha_field.shape[1]),
    "alpha_mean": alpha_field.mean(axis=0)
})
df_alpha.to_csv("FineStructure_AlphaVariation.csv", index=False)

# Plot synthetic spectra
plt.figure(figsize=(8, 5))
plt.plot(wavelengths, spectrum_base, label="Baseline Spectrum (α₀)")
plt.plot(wavelengths, synthetic_spectrum, label="Ξ-Modulated Spectrum", linestyle='--')
plt.title("Synthetic Absorption Spectrum with α(Ξ) Variation")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorption")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("FineStructure_SyntheticSpectrum.png")
plt.close()

print("Saved alpha variation data to FineStructure_AlphaVariation.csv")
print("Saved spectrum plot to FineStructure_SyntheticSpectrum.png")

