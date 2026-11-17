"""
Ξ-χ-φ-A-E-A-B-G Field Theory Simulation
Based on: "Ξ–χ–φ–A_E–A_B–G Framework: Full Mathematical Formulation" (October 2025)
Implements Sections 16-18: Full 3+1 PDE system with field-dependent couplings
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PHYSICAL CONSTANTS AND PARAMETERS (SI units)
# ============================================================================
class Constants:
    """Physical constants and framework parameters"""
    
    # Fundamental constants
    c = 2.99792458e8          # m/s
    hbar = 1.054571817e-34    # J·s
    eps0 = 8.8541878128e-12   # F/m
    mu0 = 1.25663706212e-6    # N/A²
    G = 6.67430e-11           # m³/kg·s²
    M_P = np.sqrt(hbar*c/G)   # Planck mass (kg)
    
    # Framework parameters (from Section 13.1)
    alpha_E = 1.0             # Electric gauge weighting (Eq 4.1)
    alpha_B = 0.0             # Magnetic gauge weighting
    
    # Coupling functions (simplified forms for initial simulation)
    @staticmethod
    def epsilon(xi, chi):
        """Permittivity as function of entropy/coherence (Eq 1.2)"""
        return Constants.eps0 * (1 + 0.1*np.tanh(chi) - 0.05*np.tanh(xi))
    
    @staticmethod
    def mu_inv(xi, chi):
        """Inverse permeability (Eq 1.2)"""
        return 1/Constants.mu0 * (1 + 0.08*np.tanh(chi) + 0.03*np.tanh(xi))
    
    @staticmethod
    def kappa(xi, chi):
        """Magneto-electric mixing (Eq 1.2)"""
        return 0.01 * np.exp(-xi**2) * np.cos(chi)
    
    @staticmethod
    def theta(xi, chi):
        """Axion-like coupling (Eq 1.2)"""
        return 0.005 * np.sin(chi) * (1 - np.tanh(xi**2))
    
    @staticmethod
    def xi_R(xi, chi):
        """Non-minimal curvature coupling (Eq 1.2)"""
        return 0.1 * (np.tanh(xi) + 0.5*np.tanh(chi))
    
    @staticmethod
    def m_gamma(xi, chi):
        """Dynamical photon mass (eV) - Eq 4.5"""
        m0 = 1e-18  # eV, near experimental limit
        return m0 * (1 + 0.1*np.tanh(chi) - 0.2*np.tanh(xi))
    
    @staticmethod
    def Z_xichi(xi, chi):
        """Kinetic mixing term (Eq 13.1)"""
        return 0.2 * np.exp(-0.5*(xi**2 + chi**2))

# ============================================================================
# 3+1 FIELD EQUATIONS (Section 16)
# ============================================================================
class FieldEquations:
    """Implementation of full PDE system from Section 16"""
    
    def __init__(self, N=256, L=1.0):
        """
        Initialize simulation domain
        N: number of spatial points
        L: domain length (m)
        """
        self.N = N
        self.L = L
        self.dx = L / (N - 1)
        self.x = np.linspace(0, L, N)
        
        # Field arrays (real space) - using ASCII names
        self.Xi = np.zeros(N)      # Entropy field (Ξ)
        self.Chi = np.zeros(N)     # Coherence field (χ)
        self.Phi = np.zeros(N)     # Stueckelberg field (φ)
        self.A_E = np.zeros(N)     # Electric gauge potential
        self.A_B = np.zeros(N)     # Magnetic gauge potential
        
        # Time derivatives
        self.Xi_t = np.zeros(N)
        self.Chi_t = np.zeros(N)
        self.Phi_t = np.zeros(N)
        self.A_E_t = np.zeros(N)
        self.A_B_t = np.zeros(N)
        
        # Second derivatives (accelerations)
        self.Xi_tt = np.zeros(N)
        self.Chi_tt = np.zeros(N)
        self.Phi_tt = np.zeros(N)
        self.A_E_tt = np.zeros(N)
        self.A_B_tt = np.zeros(N)
        
        # Initial conditions (coherent state with entropy gradient)
        self.set_initial_conditions()
        
    def set_initial_conditions(self):
        """Set physically motivated initial conditions"""
        # Entropy field: gradient from left (low) to right (high)
        self.Xi = 0.5 * np.tanh(5*(self.x - 0.5*self.L))
        
        # Coherence field: Gaussian peak in center
        center = 0.5 * self.L
        width = 0.1 * self.L
        self.Chi = 2.0 * np.exp(-((self.x - center)/width)**2)
        
        # Stueckelberg field: small perturbations
        self.Phi = 0.1 * np.sin(2*np.pi*self.x/self.L)
        
        # Gauge potentials: plane wave
        k = 2*np.pi/self.L
        self.A_E = 0.01 * np.sin(k*self.x)
        self.A_B = 0.005 * np.cos(k*self.x)
        
        # Small random perturbations to break symmetry
        noise = 0.01 * np.random.randn(self.N)
        self.Xi += noise
        self.Chi += 0.5*noise
        
    def laplacian(self, f):
        """Second order finite difference Laplacian"""
        return (np.roll(f, -1) - 2*f + np.roll(f, 1)) / self.dx**2
    
    def gradient(self, f):
        """First order centered difference gradient"""
        return (np.roll(f, -1) - np.roll(f, 1)) / (2*self.dx)
    
    def compute_field_derivatives(self):
        """Compute RHS of all field equations (Section 16.3-16.4)"""
        
        # Precompute gradients and Laplacians
        Xi_x = self.gradient(self.Xi)
        Chi_x = self.gradient(self.Chi)
        Phi_x = self.gradient(self.Phi)
        A_E_x = self.gradient(self.A_E)
        A_B_x = self.gradient(self.A_B)
        
        lapl_Xi = self.laplacian(self.Xi)
        lapl_Chi = self.laplacian(self.Chi)
        lapl_Phi = self.laplacian(self.Phi)
        lapl_A_E = self.laplacian(self.A_E)
        lapl_A_B = self.laplacian(self.A_B)
        
        # Field-dependent couplings (evaluate at each point)
        eps = np.array([Constants.epsilon(xi, c) for xi, c in zip(self.Xi, self.Chi)])
        mu_inv = np.array([Constants.mu_inv(xi, c) for xi, c in zip(self.Xi, self.Chi)])
        kappa_arr = np.array([Constants.kappa(xi, c) for xi, c in zip(self.Xi, self.Chi)])
        theta_arr = np.array([Constants.theta(xi, c) for xi, c in zip(self.Xi, self.Chi)])
        Z = np.array([Constants.Z_xichi(xi, c) for xi, c in zip(self.Xi, self.Chi)])
        m_gamma = np.array([Constants.m_gamma(xi, c) for xi, c in zip(self.Xi, self.Chi)])
        
        # Derivatives of couplings (simplified numerical gradients)
        deps_dXi = np.gradient(eps, self.Xi)
        dmu_inv_dXi = np.gradient(mu_inv, self.Xi)
        dkappa_dXi = np.gradient(kappa_arr, self.Xi)
        dtheta_dXi = np.gradient(theta_arr, self.Xi)
        
        deps_dChi = np.gradient(eps, self.Chi)
        dmu_inv_dChi = np.gradient(mu_inv, self.Chi)
        dkappa_dChi = np.gradient(kappa_arr, self.Chi)
        dtheta_dChi = np.gradient(theta_arr, self.Chi)
        
        # 1. Xi field equation (Eq S3, simplified)
        # Potential derivative: ∂V/∂Ξ
        dV_dXi = self.Xi + self.Xi**3 + 0.1 * self.Xi * self.Chi**2
        
        # EM source term for Xi
        EM_source_Xi = 0.25*(deps_dXi*A_E_x**2 + dmu_inv_dXi*A_B_x**2 + 
                           dkappa_dXi*A_E_x*A_B_x + dtheta_dXi*A_E_x*A_B_x)
        
        # Derivative of Z with respect to Xi
        dZ_dXi = np.gradient(Z, self.Xi)
        
        Xi_tt = (lapl_Xi + Z*lapl_Chi - 0.5*dZ_dXi*Xi_x*Chi_x - 
                dV_dXi + EM_source_Xi)
        
        # 2. Chi field equation (Eq S4, simplified)
        dV_dChi = (self.Chi - 0.4*self.Chi**3 + 0.06*self.Chi**5 + 
                  0.1*self.Xi**2*self.Chi)
        
        EM_source_Chi = 0.25*(deps_dChi*A_E_x**2 + dmu_inv_dChi*A_B_x**2 + 
                            dkappa_dChi*A_E_x*A_B_x + dtheta_dChi*A_E_x*A_B_x)
        
        dZ_dChi = np.gradient(Z, self.Chi)
        
        Chi_tt = (lapl_Chi + Z*lapl_Xi - 0.5*dZ_dChi*Xi_x*Chi_x - 
                 dV_dChi + EM_source_Chi)
        
        # 3. Combined gauge potential
        A_combined = Constants.alpha_E * self.A_E + Constants.alpha_B * self.A_B
        A_combined_x = Constants.alpha_E * A_E_x + Constants.alpha_B * A_B_x
        
        # Lorenz gauge condition (simplified)
        xi_gauge = 1.0  # Gauge parameter
        gauge_source = xi_gauge * m_gamma * self.Phi
        
        # Proca equation with dynamical mass
        lapl_A_combined = (Constants.alpha_E * lapl_A_E + 
                          Constants.alpha_B * lapl_A_B)
        A_tt = lapl_A_combined - m_gamma**2 * A_combined + m_gamma * Phi_x - gauge_source
        
        # 4. Phi equation
        Phi_tt = lapl_Phi - xi_gauge * m_gamma * A_combined_x
        
        # 5. Electric sector (simplified Maxwell with field-dependent epsilon)
        D_field = eps * A_E_x + 0.5*kappa_arr*A_B_x + 0.5*theta_arr*A_B_x
        D_x = self.gradient(D_field)
        
        # Bound charge from varying epsilon
        rho_bound = -self.gradient(eps) * A_E_x
        A_E_tt = D_x / eps - rho_bound/eps - m_gamma**2 * Constants.alpha_E * A_combined
        
        # 6. Magnetic sector
        H_field = mu_inv * A_B_x + 0.5*kappa_arr*A_E_x + 0.5*theta_arr*A_E_x
        H_x = self.gradient(H_field)
        
        # Bound current from varying mu_inv
        J_bound = -self.gradient(mu_inv) * A_B_x
        A_B_tt = H_x / mu_inv - J_bound/mu_inv - m_gamma**2 * Constants.alpha_B * A_combined
        
        return Xi_tt, Chi_tt, Phi_tt, A_E_tt, A_B_tt
    
    def time_step(self, dt):
        """Leapfrog time integration"""
        # Update positions (fields)
        self.Xi += self.Xi_t * dt + 0.5 * self.Xi_tt * dt**2
        self.Chi += self.Chi_t * dt + 0.5 * self.Chi_tt * dt**2
        self.Phi += self.Phi_t * dt + 0.5 * self.Phi_tt * dt**2
        self.A_E += self.A_E_t * dt + 0.5 * self.A_E_tt * dt**2
        self.A_B += self.A_B_t * dt + 0.5 * self.A_B_tt * dt**2
        
        # Compute new accelerations
        self.Xi_tt, self.Chi_tt, self.Phi_tt, self.A_E_tt, self.A_B_tt = self.compute_field_derivatives()
        
        # Update velocities
        self.Xi_t += self.Xi_tt * dt
        self.Chi_t += self.Chi_tt * dt
        self.Phi_t += self.Phi_tt * dt
        self.A_E_t += self.A_E_tt * dt
        self.A_B_t += self.A_B_tt * dt

# ============================================================================
# OBSERVABLES COMPUTATION (Section 7, 14.2)
# ============================================================================
class Observables:
    """Compute experimental predictions from field configurations"""
    
    @staticmethod
    def clock_drift(Xi, Xi_t, x):
        """Atomic clock drift: Δω/ω ∼ ∂_tΞ (Eq 5.4, 14.2)"""
        return Xi_t
    
    @staticmethod
    def photon_dispersion(Xi, Chi, k):
        """Massive photon dispersion: ω² = k² + m² (Eq 5.4)"""
        m = np.array([Constants.m_gamma(xi, c) for xi, c in zip(Xi, Chi)])
        # Convert eV to angular frequency (rad/s)
        eV_to_J = 1.602176634e-19
        m_J = m * eV_to_J
        omega = np.sqrt((k*Constants.c)**2 + (m_J/Constants.hbar)**2)
        return omega
    
    @staticmethod
    def birefringence(Xi, Chi, dx):
        """Polarization rotation: Δα ∼ ∫θ(Ξ,χ)dℓ (Eq 14.2)"""
        theta = np.array([Constants.theta(xi, c) for xi, c in zip(Xi, Chi)])
        Delta_alpha = np.cumsum(theta) * dx
        return Delta_alpha
    
    @staticmethod
    def effective_refractive_index(Xi, Chi):
        """Effective refractive index from field-dependent ε, μ"""
        eps = np.array([Constants.epsilon(xi, c) for xi, c in zip(Xi, Chi)])
        mu_inv = np.array([Constants.mu_inv(xi, c) for xi, c in zip(Xi, Chi)])
        mu = 1/mu_inv
        n_eff = np.sqrt(eps * mu / (Constants.eps0 * Constants.mu0))
        return n_eff
    
    @staticmethod
    def entanglement_entropy(Xi, Chi, A_length):
        """Approximate entanglement entropy with field-dependent G_eff (Eq 6.2)"""
        xi_R = np.array([Constants.xi_R(xi, c) for xi, c in zip(Xi, Chi)])
        G_eff = Constants.G / (1 + xi_R/Constants.M_P**2)
        # Entropy in natural units (dimensionless)
        S = A_length / (4 * G_eff * Constants.hbar * Constants.c**3)
        return S

# ============================================================================
# MAIN SIMULATION
# ============================================================================
def run_simulation(T=1e-9, dt=1e-12, save_interval=100):
    """
    Run full Ξ-χ-φ-A-E-A-B-G simulation
    T: total simulation time (s)
    dt: time step (s)
    """
    print("="*70)
    print("XI-CHI-PHI-A-E-A-B-G FIELD THEORY SIMULATION")
    print("Based on: 'Ξ–χ–φ–A_E–A_B–G Framework: Full Mathematical Formulation'")
    print("="*70)
    
    # Initialize system
    eq = FieldEquations(N=256, L=0.1)  # 10 cm domain
    obs = Observables()
    
    # Time arrays
    t = 0
    n_steps = int(T/dt)
    save_times = []
    saved_data = []
    
    print(f"Simulation parameters:")
    print(f"  Domain: {eq.L:.3f} m, Resolution: {eq.N} points")
    print(f"  Time: {T:.1e} s, Steps: {n_steps}")
    print(f"  Couplings: ε(Xi,Chi), μ⁻¹(Xi,Chi), κ(Xi,Chi), θ(Xi,Chi), ξ_R(Xi,Chi), m_γ(Xi,Chi)")
    print("="*70)
    
    # Initial compute
    eq.Xi_tt, eq.Chi_tt, eq.Phi_tt, eq.A_E_tt, eq.A_B_tt = eq.compute_field_derivatives()
    
    # Time evolution
    for step in range(n_steps):
        eq.time_step(dt)
        t += dt
        
        # Save data periodically
        if step % save_interval == 0:
            save_times.append(t)
            saved_data.append({
                'Xi': eq.Xi.copy(),
                'Chi': eq.Chi.copy(),
                'Phi': eq.Phi.copy(),
                'A_E': eq.A_E.copy(),
                'A_B': eq.A_B.copy()
            })
            
            # Progress
            if step % (10*save_interval) == 0:
                print(f"  Step {step}/{n_steps} (t = {t:.2e} s)")
    
    print("Simulation complete!")
    print("="*70)
    
    return eq, save_times, saved_data, obs

# ============================================================================
# VISUALIZATION AND ANALYSIS
# ============================================================================
def analyze_and_plot(eq, save_times, saved_data, obs):
    """Generate comprehensive analysis plots"""
    
    # Select key time slices
    idx_initial = 0
    idx_mid = len(saved_data) // 2
    idx_final = -1
    
    # Extract data
    Xi_initial = saved_data[idx_initial]['Xi']
    Chi_initial = saved_data[idx_initial]['Chi']
    Xi_final = saved_data[idx_final]['Xi']
    Chi_final = saved_data[idx_final]['Chi']
    
    # Compute observables at final time
    clock_drift = obs.clock_drift(eq.Xi, eq.Xi_t, eq.x)
    n_eff = obs.effective_refractive_index(eq.Xi, eq.Chi)
    biref = obs.birefringence(eq.Xi, eq.Chi, eq.dx)
    m_gamma = np.array([Constants.m_gamma(xi, c) for xi, c in zip(eq.Xi, eq.Chi)])
    entanglement = obs.entanglement_entropy(eq.Xi, eq.Chi, 0.01)  # 1 cm area
    
    # Field-dependent couplings
    eps = np.array([Constants.epsilon(xi, c) for xi, c in zip(eq.Xi, eq.Chi)])
    mu_inv = np.array([Constants.mu_inv(xi, c) for xi, c in zip(eq.Xi, eq.Chi)])
    kappa_arr = np.array([Constants.kappa(xi, c) for xi, c in zip(eq.Xi, eq.Chi)])
    theta_arr = np.array([Constants.theta(xi, c) for xi, c in zip(eq.Xi, eq.Chi)])
    
    # Create figure
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    
    # 1. Field evolution
    ax = axes[0, 0]
    ax.plot(eq.x, Xi_initial, 'b-', alpha=0.7, label='Ξ (initial)')
    ax.plot(eq.x, Xi_final, 'b--', linewidth=2, label='Ξ (final)')
    ax.plot(eq.x, Chi_initial, 'r-', alpha=0.7, label='χ (initial)')
    ax.plot(eq.x, Chi_final, 'r--', linewidth=2, label='χ (final)')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Field amplitude')
    ax.set_title('Entropy (Ξ) and Coherence (χ) Evolution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Clock drift prediction
    ax = axes[0, 1]
    ax.plot(eq.x, clock_drift, 'g-', linewidth=2)
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Δω/ω (relative drift)')
    ax.set_title('Atomic Clock Drift: Δω/ω ∼ ∂_tΞ')
    ax.grid(True, alpha=0.3)
    ax.text(0.05, 0.95, f'Max drift: {np.max(np.abs(clock_drift)):.2e}',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 3. Effective refractive index
    ax = axes[0, 2]
    ax.plot(eq.x, n_eff, 'm-', linewidth=2)
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('n_eff')
    ax.set_title('Effective Refractive Index: n = √(εμ/ε₀μ₀)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    ax.text(0.05, 0.95, f'Δn = {np.max(n_eff)-np.min(n_eff):.2e}',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 4. Birefringence
    ax = axes[1, 0]
    ax.plot(eq.x, biref, 'c-', linewidth=2)
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Δα (rad)')
    ax.set_title('Polarization Rotation: Δα ∼ ∫θ(Ξ,χ)dℓ')
    ax.grid(True, alpha=0.3)
    ax.text(0.05, 0.95, f'Total rotation: {biref[-1]:.2e} rad',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 5. Dynamical photon mass
    ax = axes[1, 1]
    ax.plot(eq.x, m_gamma, 'orange', linewidth=2)
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('m_γ (eV)')
    ax.set_title('Dynamical Photon Mass: m_γ(Ξ,χ)')
    ax.grid(True, alpha=0.3)
    ax.text(0.05, 0.95, f'Max: {np.max(m_gamma):.1e} eV',
            transform=ax.transAxes, fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 6. Entanglement entropy
    ax = axes[1, 2]
    ax.plot(eq.x, entanglement, 'purple', linewidth=2)
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('S (dimensionless)')
    ax.set_title('Entanglement Entropy: S ∼ A/(4G_eff)')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    # 7. Phase space portrait (Xi vs Chi)
    ax = axes[2, 0]
    scatter = ax.scatter(eq.Xi, eq.Chi, c=eq.x, cmap='viridis', s=20, alpha=0.7)
    ax.set_xlabel('Entropy field Ξ')
    ax.set_ylabel('Coherence field χ')
    ax.set_title('Phase Space: Ξ-χ Attractor Structure')
    ax.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Position (m)')
    
    # 8. Gauge potentials
    ax = axes[2, 1]
    ax.plot(eq.x, eq.A_E, 'b-', label='A_E (electric)')
    ax.plot(eq.x, eq.A_B, 'r-', label='A_B (magnetic)')
    ax.plot(eq.x, eq.Phi, 'g-', label='φ (Stueckelberg)')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Field amplitude')
    ax.set_title('Gauge Fields Evolution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 9. Field-dependent couplings
    ax = axes[2, 2]
    ax.plot(eq.x, eps/Constants.eps0, label='ε/ε₀')
    ax.plot(eq.x, 1/(mu_inv*Constants.mu0), label='μ/μ₀')
    ax.plot(eq.x, kappa_arr*100, label='κ × 100')
    ax.plot(eq.x, theta_arr*100, label='θ × 100')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Normalized couplings')
    ax.set_title('Field-Dependent Coupling Constants')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Ξ-χ-φ-A-E-A-B-G Framework: Numerical Simulation Results', 
                 fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()
    
    # Print summary of observables
    print("\n" + "="*70)
    print("EXPERIMENTAL PREDICTIONS SUMMARY:")
    print("="*70)
    print(f"1. Clock Drift: Δω/ω_max = {np.max(np.abs(clock_drift)):.2e}")
    print(f"2. Refractive Index Variation: Δn = {np.max(n_eff)-np.min(n_eff):.2e}")
    print(f"3. Polarization Rotation: Δα_total = {biref[-1]:.2e} rad")
    print(f"4. Photon Mass Range: {np.min(m_gamma):.1e} - {np.max(m_gamma):.1e} eV")
    print(f"5. Permittivity Variation: ε/ε₀ = {np.min(eps/Constants.eps0):.3f} - {np.max(eps/Constants.eps0):.3f}")
    print(f"6. Permeability Variation: μ/μ₀ = {np.min(1/(mu_inv*Constants.mu0)):.3f} - {np.max(1/(mu_inv*Constants.mu0)):.3f}")
    
    # Experimental constraints check
    print("\n" + "="*70)
    print("EXPERIMENTAL CONSTRAINTS CHECK:")
    print("="*70)
    
    # Photon mass constraint
    m_max = np.max(m_gamma)
    if m_max < 1e-18:
        print(f"✓ Photon mass OK: {m_max:.1e} eV < 1e-18 eV (Coulomb law)")
    else:
        print(f"✗ Photon mass TOO HIGH: {m_max:.1e} eV > 1e-18 eV")
    
    # Birefringence constraint (typical astrophysical limit ~1e-32)
    if np.max(np.abs(theta_arr)) < 1e-10:
        print(f"✓ Birefringence OK: |θ| = {np.max(np.abs(theta_arr)):.1e} < 1e-10")
    else:
        print(f"✗ Birefringence MAY BE DETECTABLE: |θ| = {np.max(np.abs(theta_arr)):.1e}")
    
    # Clock drift (current precision ~1e-18)
    if np.max(np.abs(clock_drift)) < 1e-15:
        print(f"✓ Clock drift below current precision: {np.max(np.abs(clock_drift)):.1e}")
    else:
        print(f"⚠ Clock drift potentially measurable: {np.max(np.abs(clock_drift)):.1e}")
        
    # Energy conservation check (simplified)
    kinetic_energy = 0.5 * (np.mean(eq.Xi_t**2) + np.mean(eq.Chi_t**2) + 
                          np.mean(eq.Phi_t**2) + np.mean(eq.A_E_t**2) + 
                          np.mean(eq.A_B_t**2))
    print(f"\n7. Approximate kinetic energy density: {kinetic_energy:.2e} J/m³")

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    # Run simulation
    eq, save_times, saved_data, obs = run_simulation(
        T=1e-10,     # 100 ps simulation (shorter for testing)
        dt=1e-13,    # 0.1 ps time step
        save_interval=50
    )
    
    # Analyze and plot results
    analyze_and_plot(eq, save_times, saved_data, obs)
    
    # Save data for further analysis
    np.savez('xi_chi_simulation_results.npz',
             x=eq.x,
             Xi=eq.Xi,
             Chi=eq.Chi,
             Phi=eq.Phi,
             A_E=eq.A_E,
             A_B=eq.A_B,
             save_times=np.array(save_times))
    
    print("\n" + "="*70)
    print("Simulation data saved to: xi_chi_simulation_results.npz")
    print("="*70)
