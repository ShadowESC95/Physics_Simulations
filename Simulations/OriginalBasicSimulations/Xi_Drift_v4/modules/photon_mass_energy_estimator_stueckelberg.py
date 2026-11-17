# Define photon mass and gauge field A_x, A_y and Stueckelberg scalar φ
photon_mass = 1e-3  # arbitrary test mass in normalized units

# Initialize vector potential A_mu (2D: A_x, A_y)
A_x = np.random.normal(0, 0.01, xi_field.shape)
A_y = np.random.normal(0, 0.01, xi_field.shape)

# Initialize Stueckelberg scalar field φ
phi = np.random.normal(0, 0.01, xi_field.shape)

# Compute derivative of φ (∂x φ, ∂y φ)
grad_phi_x = np.gradient(phi, axis=1)
grad_phi_y = np.gradient(phi, axis=0)

# Stueckelberg-compensated vector field: A_mu + (1/m) ∂μ φ
Ax_stueck = A_x + (1 / photon_mass) * grad_phi_x
Ay_stueck = A_y + (1 / photon_mass) * grad_phi_y

# Compute gauge-invariant mass term: (A + ∂φ/m)^2
mass_term = photon_mass**2 * (Ax_stueck**2 + Ay_stueck**2)
total_mass_energy = np.sum(mass_term)

total_mass_energy
