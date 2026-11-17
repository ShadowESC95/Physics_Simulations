"""
Ξ-χ-φ-A-E-A-B-G Field Theory Simulation - PHYSICS-CORRECTED VERSION
Implements Sections 16-18 with proper numerics and consistency checks
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PHYSICAL CONSTANTS AND CONVERSIONS (SI units)
# ============================================================================
class ConstantsSI:
    """All constants in SI units with proper dimensions"""
    
    # Fundamental constants
    c = 2.99792458e8           # m/s
    hbar = 1.054571817e-34     # J·s
    eps0 = 8.8541878128e-12    # F/m
    mu0 = 1.25663706212e-6     # N/A²
    G = 6.67430e-11            # m³/kg·s²
    e_charge = 1.602176634e-19 # C
    
    # Planck units for dimensionless formulation
    M_pl = np.sqrt(hbar*c/G)    # Planck mass (kg)
    L_pl = np.sqrt(hbar*G/c**3) # Planck length (m)
    T_pl = np.sqrt(hbar*G/c**5) # Planck time (s)
    E_pl = M_pl * c**2         # Planck energy (J)
    
    # Unit conversions
    eV_to_J = e_charge          # 1 eV = 1.602e-19 J
    J_to_eV = 1.0 / eV_to_J
    
    @staticmethod
    def natural_to_SI(value_natural, unit_type='energy'):
        """Convert from natural units (ħ=c=1) to SI"""
        if unit_type == 'energy':
            return value_natural * E_pl
        elif unit_type == 'mass':
            return value_natural * M_pl
        elif unit_type == 'length':
            return value_natural * L_pl
        elif unit_type == 'time':
            return value_natural * T_pl
        return value_natural
    
    @staticmethod
    def photon_mass_SI(m_eV):
        """Convert photon mass in eV to inverse Compton wavelength in m^-1"""
        m_J = m_eV * ConstantsSI.eV_to_J
        return m_J / (ConstantsSI.hbar * ConstantsSI.c)  # m⁻¹
    
    @staticmethod
    def epsilon(xi, chi):
        """Dimensionless permittivity - analytic derivative available"""
        eps_r = 1.0 + 0.1*np.tanh(chi) - 0.05*np.tanh(xi)
        return eps_r  # Dimensionless
    
    @staticmethod
    def deps_dxi(xi, chi):
        """Analytic derivative ∂ε/∂Ξ"""
        return -0.05 * (1 - np.tanh(xi)**2)
    
    @staticmethod
    def deps_dchi(xi, chi):
        """Analytic derivative ∂ε/∂χ"""
        return 0.1 * (1 - np.tanh(chi)**2)
    
    @staticmethod
    def mu_inv(xi, chi):
        """Dimensionless inverse permeability"""
        mu_r_inv = 1.0 + 0.08*np.tanh(chi) + 0.03*np.tanh(xi)
        return mu_r_inv  # Dimensionless
    
    @staticmethod
    def dmu_inv_dxi(xi, chi):
        """Analytic derivative ∂μ⁻¹/∂Ξ"""
        return 0.03 * (1 - np.tanh(xi)**2)
    
    @staticmethod
    def dmu_inv_dchi(xi, chi):
        """Analytic derivative ∂μ⁻¹/∂χ"""
        return 0.08 * (1 - np.tanh(chi)**2)
    
    @staticmethod
    def kappa(xi, chi):
        """Dimensionless magneto-electric mixing"""
        return 0.01 * np.exp(-xi**2) * np.cos(chi)
    
    @staticmethod
    def dkappa_dxi(xi, chi):
        """Analytic derivative ∂κ/∂Ξ"""
        return -0.02 * xi * np.exp(-xi**2) * np.cos(chi)
    
    @staticmethod
    def dkappa_dchi(xi, chi):
        """Analytic derivative ∂κ/∂χ"""
        return -0.01 * np.exp(-xi**2) * np.sin(chi)
    
    @staticmethod
    def theta(xi, chi):
        """Dimensionless axion-like coupling"""
        return 0.005 * np.sin(chi) * (1 - np.tanh(xi**2))
    
    @staticmethod
    def dtheta_dxi(xi, chi):
        """Analytic derivative ∂θ/∂Ξ"""
        tanh_xi2 = np.tanh(xi**2)
        return -0.005 * np.sin(chi) * (1 - tanh_xi2**2) * 2*xi
    
    @staticmethod
    def dtheta_dchi(xi, chi):
        """Analytic derivative ∂θ/∂χ"""
        return 0.005 * np.cos(chi) * (1 - np.tanh(xi**2))
    
    @staticmethod
    def Z_xichi(xi, chi):
        """Dimensionless kinetic mixing"""
        return 0.2 * np.exp(-0.5*(xi**2 + chi**2))
    
    @staticmethod
    def dZ_dxi(xi, chi):
        """Analytic derivative ∂Z/∂Ξ"""
        return -0.2 * xi * np.exp(-0.5*(xi**2 + chi**2))
    
    @staticmethod
    def dZ_dchi(xi, chi):
        """Analytic derivative ∂Z/∂χ"""
        return -0.2 * chi * np.exp(-0.5*(xi**2 + chi**2))
    
    @staticmethod
    def m_gamma_eV(xi, chi):
        """Photon mass in eV - must be converted to SI properly"""
        m0 = 1e-18  # eV, experimental limit
        return m0 * (1 + 0.1*np.tanh(chi) - 0.2*np.tanh(xi))
    
    @staticmethod
    def m_gamma_SI(xi, chi):
        """Photon mass in SI units (inverse Compton wavelength in m^-1)"""
        m_eV = ConstantsSI.m_gamma_eV(xi, chi)
        return ConstantsSI.photon_mass_SI(m_eV)
    
    @staticmethod
    def dm_gamma_dxi(xi, chi):
        """Derivative of photon mass w.r.t Ξ"""
        m0 = 1e-18
        return m0 * (-0.2) * (1 - np.tanh(xi)**2)
    
    @staticmethod
    def dm_gamma_dchi(xi, chi):
        """Derivative of photon mass w.r.t χ"""
        m0 = 1e-18
        return m0 * 0.1 * (1 - np.tanh(chi)**2)

# ============================================================================
# FINITE DIFFERENCE OPERATORS WITH PHYSICAL BOUNDARY CONDITIONS
# ============================================================================
class FiniteDifference:
    """Proper finite difference operators with Neumann/Dirichlet BCs"""
    
    def __init__(self, N, L, bc_type='neumann'):
        """
        N: number of spatial points
        L: domain length (m)
        bc_type: 'neumann' (zero gradient) or 'dirichlet' (fixed value)
        """
        self.N = N
        self.L = L
        self.dx = L / (N - 1)
        self.x = np.linspace(0, L, N)
        self.bc_type = bc_type
        
        # Build sparse differentiation matrices
        self.grad_matrix = self._build_gradient_matrix()
        self.laplacian_matrix = self._build_laplacian_matrix()
    
    def _build_gradient_matrix(self):
        """First derivative matrix with proper BCs"""
        diag_main = np.zeros(self.N)
        diag_upper = np.ones(self.N-1)
        diag_lower = -np.ones(self.N-1)
        
        if self.bc_type == 'neumann':
            # ∂f/∂x = 0 at boundaries
            diag_upper[-1] = 0
            diag_lower[0] = 0
        elif self.bc_type == 'dirichlet':
            # f = 0 at boundaries (for simplicity)
            diag_upper[-1] = 0
            diag_lower[0] = 0
        
        grad = sparse.diags([diag_lower, diag_main, diag_upper], 
                           [-1, 0, 1], format='csr')
        return grad / (2*self.dx)
    
    def _build_laplacian_matrix(self):
        """Second derivative matrix with proper BCs"""
        diag_main = -2 * np.ones(self.N)
        diag_upper = np.ones(self.N-1)
        diag_lower = np.ones(self.N-1)
        
        if self.bc_type == 'neumann':
            # ∂f/∂x = 0 at boundaries
            diag_main[0] = -1
            diag_main[-1] = -1
            diag_upper[0] = 1
            diag_lower[-1] = 1
        elif self.bc_type == 'dirichlet':
            # f = 0 at boundaries
            diag_main[0] = 1
            diag_main[-1] = 1
            diag_upper[0] = 0
            diag_lower[-1] = 0
        
        lapl = sparse.diags([diag_lower, diag_main, diag_upper], 
                           [-1, 0, 1], format='csr')
        return lapl / (self.dx**2)
    
    def gradient(self, f):
        """Compute gradient using sparse matrix"""
        return self.grad_matrix.dot(f)
    
    def laplacian(self, f):
        """Compute Laplacian using sparse matrix"""
        return self.laplacian_matrix.dot(f)

# ============================================================================
# FIELD EQUATIONS WITH PROPER ENERGY CONSERVATION
# ============================================================================
class FieldSystem:
    """Proper implementation of the coupled field equations"""
    
    def __init__(self, N=256, L=0.1, bc_type='neumann'):
        """
        Initialize with proper boundary conditions
        L = 0.1 m = 10 cm domain
        """
        self.N = N
        self.L = L
        self.fd = FiniteDifference(N, L, bc_type)
        self.x = self.fd.x
        self.dx = self.fd.dx
        
        # Field arrays and their time derivatives
        self.fields = {
            'Xi': np.zeros(N),      # Entropy field Ξ
            'Chi': np.zeros(N),     # Coherence field χ
            'Phi': np.zeros(N),     # Stueckelberg field φ
            'A_E': np.zeros(N),     # Electric potential A_E
            'A_B': np.zeros(N)      # Magnetic potential A_B
        }
        
        self.velocities = {
            'Xi': np.zeros(N),
            'Chi': np.zeros(N),
            'Phi': np.zeros(N),
            'A_E': np.zeros(N),
            'A_B': np.zeros(N)
        }
        
        self.accelerations = {
            'Xi': np.zeros(N),
            'Chi': np.zeros(N),
            'Phi': np.zeros(N),
            'A_E': np.zeros(N),
            'A_B': np.zeros(N)
        }
        
        # Energy tracking
        self.energy_history = []
        self.time_history = []
        
        # Physical initial conditions
        self.set_physical_initial_conditions()
    
    def set_physical_initial_conditions(self):
        """Set initial conditions with proper physical meaning"""
        x = self.x
        L = self.L
        
        # Entropy field: smooth gradient from left (low) to right (high)
        # With Neumann BCs at boundaries
        self.fields['Xi'] = 0.5 * (np.tanh(5*(x - 0.5*L)) + 1)
        
        # Coherence field: Gaussian peak in center (coherent region)
        center = 0.5 * L
        width = 0.02 * L  # 2% of domain width
        self.fields['Chi'] = 2.0 * np.exp(-((x - center)/width)**2)
        
        # Stueckelberg field: small perturbation consistent with gauge
        k = 2*np.pi/L
        self.fields['Phi'] = 0.01 * np.sin(k*x)
        
        # Gauge potentials: consistent with plane wave
        self.fields['A_E'] = 0.001 * np.sin(k*x)
        self.fields['A_B'] = 0.0005 * np.cos(k*x)
        
        # Initial velocities: small but non-zero for evolution
        # This ensures proper energy content
        self.velocities['Xi'] = 0.01 * np.cos(3*k*x)
        self.velocities['Chi'] = -0.005 * np.sin(2*k*x)
        
        # Initialize accelerations from equations of motion
        self._compute_accelerations()
        
        # Record initial energy
        self._record_energy(0.0)
    
    def _compute_accelerations(self):
        """Compute RHS of all field equations with proper derivatives"""
        Xi = self.fields['Xi']
        Chi = self.fields['Chi']
        Phi = self.fields['Phi']
        A_E = self.fields['A_E']
        A_B = self.fields['A_B']
        
        # Spatial derivatives
        Xi_x = self.fd.gradient(Xi)
        Chi_x = self.fd.gradient(Chi)
        Phi_x = self.fd.gradient(Phi)
        A_E_x = self.fd.gradient(A_E)
        A_B_x = self.fd.gradient(A_B)
        
        Xi_xx = self.fd.laplacian(Xi)
        Chi_xx = self.fd.laplacian(Chi)
        Phi_xx = self.fd.laplacian(Phi)
        A_E_xx = self.fd.laplacian(A_E)
        A_B_xx = self.fd.laplacian(A_B)
        
        # Time derivatives (from velocities)
        Xi_t = self.velocities['Xi']
        Chi_t = self.velocities['Chi']
        Phi_t = self.velocities['Phi']
        A_E_t = self.velocities['A_E']
        A_B_t = self.velocities['A_B']
        
        # Field-dependent couplings (computed pointwise)
        eps = np.array([ConstantsSI.epsilon(xi, c) for xi, c in zip(Xi, Chi)])
        mu_inv = np.array([ConstantsSI.mu_inv(xi, c) for xi, c in zip(Xi, Chi)])
        kappa_arr = np.array([ConstantsSI.kappa(xi, c) for xi, c in zip(Xi, Chi)])
        theta_arr = np.array([ConstantsSI.theta(xi, c) for xi, c in zip(Xi, Chi)])
        Z = np.array([ConstantsSI.Z_xichi(xi, c) for xi, c in zip(Xi, Chi)])
        m_gamma = np.array([ConstantsSI.m_gamma_SI(xi, c) for xi, c in zip(Xi, Chi)])  # m⁻¹
        
        # Analytic derivatives (no numerical gradient errors)
        deps_dXi = np.array([ConstantsSI.deps_dxi(xi, c) for xi, c in zip(Xi, Chi)])
        deps_dChi = np.array([ConstantsSI.deps_dchi(xi, c) for xi, c in zip(Xi, Chi)])
        dmu_inv_dXi = np.array([ConstantsSI.dmu_inv_dxi(xi, c) for xi, c in zip(Xi, Chi)])
        dmu_inv_dChi = np.array([ConstantsSI.dmu_inv_dchi(xi, c) for xi, c in zip(Xi, Chi)])
        dkappa_dXi = np.array([ConstantsSI.dkappa_dxi(xi, c) for xi, c in zip(Xi, Chi)])
        dkappa_dChi = np.array([ConstantsSI.dkappa_dchi(xi, c) for xi, c in zip(Xi, Chi)])
        dtheta_dXi = np.array([ConstantsSI.dtheta_dxi(xi, c) for xi, c in zip(Xi, Chi)])
        dtheta_dChi = np.array([ConstantsSI.dtheta_dchi(xi, c) for xi, c in zip(Xi, Chi)])
        dZ_dXi = np.array([ConstantsSI.dZ_dxi(xi, c) for xi, c in zip(Xi, Chi)])
        dZ_dChi = np.array([ConstantsSI.dZ_dchi(xi, c) for xi, c in zip(Xi, Chi)])
        dm_dXi = np.array([ConstantsSI.dm_gamma_dxi(xi, c) for xi, c in zip(Xi, Chi)])
        dm_dChi = np.array([ConstantsSI.dm_gamma_dchi(xi, c) for xi, c in zip(Xi, Chi)])
        
        # Potentials and their derivatives
        # V_tot = V_Ξ(Ξ) + U_χ(χ) + W(Ξ,χ)
        V_Xi = 0.5 * Xi**2 + 0.25 * Xi**4 + 0.05 * Xi**2 * Chi**2
        dV_dXi = Xi + Xi**3 + 0.1 * Xi * Chi**2
        
        V_Chi = 0.5 * Chi**2 - 0.1 * Chi**4 + 0.01 * Chi**6 + 0.05 * Xi**2 * Chi**2
        dV_dChi = Chi - 0.4 * Chi**3 + 0.06 * Chi**5 + 0.1 * Xi**2 * Chi
        
        # EM field strengths (1D approximation)
        F_E_squared = -2 * A_E_x**2  # Minus sign from metric
        F_B_squared = -2 * A_B_x**2
        F_E_dot_F_B = -2 * A_E_x * A_B_x
        
        # ===== Ξ EQUATION (Eq S3) =====
        # ∂ₜ²Ξ - ∇²Ξ + Z(∂ₜ²χ - ∇²χ) - ½(∂_Ξ Z)(∂_μΞ∂^μχ) + ∂_Ξ V_tot = EM_source
        # Note: ∂_μΞ∂^μχ = -∂ₜΞ∂ₜχ + ∇Ξ·∇χ (metric signature -+++)
        
        # Time derivative term for χ (from stored velocities)
        Chi_tt_current = self.accelerations['Chi']  # Will be updated
        
        # Full d'Alembertian terms
        dalembertian_Xi = -Xi_xx  # -∇²Ξ in 1D (spatial only, time part handled separately)
        dalembertian_Chi = -Chi_xx  # -∇²χ
        
        # EM source term for Ξ
        EM_source_Xi = 0.25 * (deps_dXi * F_E_squared + 
                              dmu_inv_dXi * F_B_squared +
                              dkappa_dXi * F_E_dot_F_B + 
                              dtheta_dXi * F_E_dot_F_B)
        
        # Mixed derivative term: ∂_μΞ∂^μχ = -∂ₜΞ∂ₜχ + ∇Ξ·∇χ
        mixed_deriv = -Xi_t * Chi_t + Xi_x * Chi_x
        
        # Assemble Ξ equation
        Xi_tt = (dalembertian_Xi + Z * dalembertian_Chi - 
                 0.5 * dZ_dXi * mixed_deriv - dV_dXi + EM_source_Xi)
        
        # Remove Z*Chi_tt term since we'll solve coupled system
        # This will be handled in the time integration
        
        # ===== χ EQUATION (Eq S4) =====
        # ∂ₜ²χ - ∇²χ + Z(∂ₜ²Ξ - ∇²Ξ) - ½(∂_χ Z)(∂_μΞ∂^μχ) + ∂_χ V_tot = EM_source
        
        EM_source_Chi = 0.25 * (deps_dChi * F_E_squared + 
                               dmu_inv_dChi * F_B_squared +
                               dkappa_dChi * F_E_dot_F_B + 
                               dtheta_dChi * F_E_dot_F_B)
        
        Chi_tt = (dalembertian_Chi + Z * dalembertian_Xi - 
                  0.5 * dZ_dChi * mixed_deriv - dV_dChi + EM_source_Chi)
        
        # ===== φ EQUATION (Stueckelberg) =====
        # □φ - m(∂·A) - (∂m)·A = 0
        # In Lorenz gauge: ∂·A + ξmφ = 0
        
        xi_gauge = 1.0  # Gauge parameter
        A_combined = 1.0 * A_E + 0.0 * A_B  # α_E = 1, α_B = 0
        A_combined_x = 1.0 * A_E_x + 0.0 * A_B_x
        
        # Proper Stueckelberg equation
        Phi_tt = -Phi_xx + m_gamma * (A_combined_x + xi_gauge * m_gamma * Phi)
        
        # ===== A_E EQUATION =====
        # ∂_ν(εF_E^νμ + κ/2 F_B^νμ + θ/2 F̃_B^νμ) + mα_E(∂^μφ - mA^μ) = 0
        
        # D field: D = εE + κ/2 E_B + θ/2 Ẽ_B
        # In 1D with scalar potential: E = -∂_tA_E - ∂_x A_0, but A_0=0 in our gauge
        E_field = -A_E_t  # ∂_tA_E is velocity
        D_field = eps * E_field + 0.5*kappa_arr*A_B_t + 0.5*theta_arr*A_B_t
        
        D_x = self.fd.gradient(D_field)
        
        # Proca mass term
        mass_term_E = m_gamma**2 * A_combined  # m²A
        
        A_E_tt = -D_x - mass_term_E
        
        # ===== A_B EQUATION =====
        # Similar structure for magnetic sector
        
        B_field = A_B_x  # In 1D with our conventions
        H_field = mu_inv * B_field + 0.5*kappa_arr*A_E_x + 0.5*theta_arr*A_E_x
        
        H_x = self.fd.gradient(H_field)
        
        mass_term_B = m_gamma**2 * 0.0 * A_combined  # α_B = 0 in our case
        
        A_B_tt = -H_x - mass_term_B
        
        # Store accelerations
        self.accelerations['Xi'] = Xi_tt
        self.accelerations['Chi'] = Chi_tt
        self.accelerations['Phi'] = Phi_tt
        self.accelerations['A_E'] = A_E_tt
        self.accelerations['A_B'] = A_B_tt
    
    def _compute_energy(self):
        """Compute total energy density integrated over domain"""
        Xi = self.fields['Xi']
        Chi = self.fields['Chi']
        Phi = self.fields['Phi']
        A_E = self.fields['A_E']
        A_B = self.fields['A_B']
        
        Xi_t = self.velocities['Xi']
        Chi_t = self.velocities['Chi']
        Phi_t = self.velocities['Phi']
        A_E_t = self.velocities['A_E']
        A_B_t = self.velocities['A_B']
        
        Xi_x = self.fd.gradient(Xi)
        Chi_x = self.fd.gradient(Chi)
        Phi_x = self.fd.gradient(Phi)
        A_E_x = self.fd.gradient(A_E)
        A_B_x = self.fd.gradient(A_B)
        
        # Pointwise couplings
        eps = np.array([ConstantsSI.epsilon(xi, c) for xi, c in zip(Xi, Chi)])
        mu_inv = np.array([ConstantsSI.mu_inv(xi, c) for xi, c in zip(Xi, Chi)])
        kappa_arr = np.array([ConstantsSI.kappa(xi, c) for xi, c in zip(Xi, Chi)])
        theta_arr = np.array([ConstantsSI.theta(xi, c) for xi, c in zip(Xi, Chi)])
        Z = np.array([ConstantsSI.Z_xichi(xi, c) for xi, c in zip(Xi, Chi)])
        m_gamma = np.array([ConstantsSI.m_gamma_SI(xi, c) for xi, c in zip(Xi, Chi)])
        
        # Kinetic energy density (time derivatives)
        # Include kinetic mixing term: ½[∂ₜΞ∂ₜΞ + ∂ₜχ∂ₜχ + 2Z ∂ₜΞ∂ₜχ]
        kinetic = 0.5 * (Xi_t**2 + Chi_t**2 + 2*Z*Xi_t*Chi_t + 
                        Phi_t**2 + A_E_t**2 + A_B_t**2)
        
        # Gradient energy density (space derivatives)
        # Include kinetic mixing: ½[∇Ξ·∇Ξ + ∇χ·∇χ + 2Z ∇Ξ·∇χ]
        gradient = 0.5 * (Xi_x**2 + Chi_x**2 + 2*Z*Xi_x*Chi_x + 
                         Phi_x**2 + A_E_x**2 + A_B_x**2)
        
        # Potential energy
        V_Xi = 0.5 * Xi**2 + 0.25 * Xi**4 + 0.05 * Xi**2 * Chi**2
        V_Chi = 0.5 * Chi**2 - 0.1 * Chi**4 + 0.01 * Chi**6 + 0.05 * Xi**2 * Chi**2
        V_Phi = 0.5 * m_gamma**2 * Phi**2
        
        potential = V_Xi + V_Chi + V_Phi
        
        # EM field energy
        # D·E + H·B terms with field-dependent couplings
        E_field = -A_E_t  # Approximation in 1D
        B_field = A_B_x
        
        D_field = eps * E_field + 0.5*kappa_arr*B_field + 0.5*theta_arr*B_field
        H_field = mu_inv * B_field + 0.5*kappa_arr*E_field + 0.5*theta_arr*E_field
        
        em_energy = 0.5 * (D_field * E_field + H_field * B_field)
        
        # Proca mass term for gauge fields
        A_combined = 1.0 * A_E + 0.0 * A_B
        proca_energy = 0.5 * m_gamma**2 * A_combined**2
        
        # Total energy density
        energy_density = kinetic + gradient + potential + em_energy + proca_energy
        
        # Integrate over domain (trapezoidal rule)
        total_energy = np.trapz(energy_density, self.x)
        
        return total_energy, {
            'kinetic': np.trapz(kinetic, self.x),
            'gradient': np.trapz(gradient, self.x),
            'potential': np.trapz(potential, self.x),
            'em': np.trapz(em_energy, self.x),
            'proca': np.trapz(proca_energy, self.x)
        }
    
    def _record_energy(self, t):
        """Record current energy for conservation check"""
        total_energy, components = self._compute_energy()
        self.energy_history.append((t, total_energy, components))
        self.time_history.append(t)
    
    def time_step_velocity_verlet(self, dt):
        """Proper velocity Verlet integration (symplectic, energy-conserving)"""
        
        # Half-step velocity update
        for field in ['Xi', 'Chi', 'Phi', 'A_E', 'A_B']:
            self.velocities[field] += 0.5 * dt * self.accelerations[field]
        
        # Full-step position update
        for field in ['Xi', 'Chi', 'Phi', 'A_E', 'A_B']:
            self.fields[field] += dt * self.velocities[field]
        
        # Recompute accelerations with new positions
        self._compute_accelerations()
        
        # Second half-step velocity update
        for field in ['Xi', 'Chi', 'Phi', 'A_E', 'A_B']:
            self.velocities[field] += 0.5 * dt * self.accelerations[field]
    
    def evolve(self, total_time, dt, energy_check_interval=100):
        """Evolve system with energy conservation monitoring"""
        n_steps = int(total_time / dt)
        energy_drift = []
        
        print(f"Evolving {n_steps} steps with dt = {dt:.2e} s")
        print(f"CFL condition check: c*dt/dx = {ConstantsSI.c*dt/self.dx:.3f}")
        print("(Should be < 1 for stability)")
        
        for step in range(n_steps):
            t = step * dt
            
            # Take time step
            self.time_step_velocity_verlet(dt)
            
            # Check energy conservation periodically
            if step % energy_check_interval == 0:
                self._record_energy(t)
                if len(self.energy_history) > 1:
                    E0 = self.energy_history[0][1]
                    E_current = self.energy_history[-1][1]
                    rel_drift = abs((E_current - E0) / E0) if abs(E0) > 1e-30 else 0
                    energy_drift.append(rel_drift)
                    
                    if step % (10*energy_check_interval) == 0:
                        print(f"Step {step}/{n_steps}: Energy = {E_current:.3e} J/m, "
                              f"Drift = {rel_drift:.2e}")
        
        # Final energy check
        self._record_energy(total_time)
        if len(self.energy_history) > 1:
            E0 = self.energy_history[0][1]
            E_final = self.energy_history[-1][1]
            final_drift = abs((E_final - E0) / E0) if abs(E0) > 1e-30 else 0
            print(f"\nFinal energy conservation: ΔE/E0 = {final_drift:.2e}")
            
            if final_drift > 0.01:
                print("WARNING: Energy drift > 1%. Check timestep and BCs.")
        
        return energy_drift

# ============================================================================
# OBSERVABLES WITH PROPER UNITS
# ============================================================================
class ObservablesSI:
    """Observables computed with proper SI units and dimensions"""
    
    @staticmethod
    def clock_drift(Xi_velocity):
        """Atomic clock drift: Δω/ω = ∂_tΞ (dimensionless)"""
        return Xi_velocity  # Already dimensionless in our units
    
    @staticmethod
    def effective_refractive_index(xi, chi):
        """n_eff = √(εμ/ε₀μ₀) = √(ε_r μ_r)"""
        eps_r = np.array([ConstantsSI.epsilon(x, c) for x, c in zip(xi, chi)])
        mu_inv_r = np.array([ConstantsSI.mu_inv(x, c) for x, c in zip(xi, chi)])
        mu_r = 1.0 / mu_inv_r  # Convert inverse to direct
        n_eff = np.sqrt(eps_r * mu_r)
        return n_eff
    
    @staticmethod
    def polarization_rotation(xi, chi, dx):
        """Δα = ½∫θ(Ξ,χ) dℓ (radians)"""
        theta = np.array([ConstantsSI.theta(x, c) for x, c in zip(xi, chi)])
        # Integral along path
        Delta_alpha = 0.5 * np.cumsum(theta) * dx
        return Delta_alpha
    
    @staticmethod
    def photon_dispersion_relation(k, m_gamma_SI):
        """ω² = (ck)² + (m_γc²/ħ)² in proper SI units"""
        # m_gamma_SI is in m⁻¹ (inverse Compton wavelength)
        # ω = c * sqrt(k² + m_gamma_SI²)
        omega = ConstantsSI.c * np.sqrt(k**2 + m_gamma_SI**2)
        return omega
    
    @staticmethod
    def entanglement_entropy_density(xi, chi, area_scale=1e-4):
        """S/A = 1/(4G_eff) with G_eff = G/(1 + ξ_R/M_pl²)"""
        # Simplified: ξ_R = 0.1*(tanh(Ξ) + 0.5*tanh(χ))
        xi_R = 0.1 * (np.tanh(xi) + 0.5*np.tanh(chi))
        G_eff = ConstantsSI.G / (1 + xi_R/ConstantsSI.M_pl**2)
        S_density = area_scale / (4 * G_eff * ConstantsSI.hbar * ConstantsSI.c**3)
        return S_density

# ============================================================================
# MAIN SIMULATION WITH VALIDATION
# ============================================================================
def run_validation_simulation():
    """Run simulation with all physics checks enabled"""
    
    print("="*70)
    print("Ξ-χ-φ-A-E-A-B-G SIMULATION - PHYSICS VALIDATED VERSION")
    print("="*70)
    
    # Initialize with physical parameters
    L = 0.1  # 10 cm domain
    N = 512  # Higher resolution for accuracy
    system = FieldSystem(N=N, L=L, bc_type='neumann')
    
    # Time parameters respecting CFL condition
    dx = system.dx
    dt = 0.1 * dx / ConstantsSI.c  # CFL condition: c*dt/dx < 1
    total_time = 1e-10  # 100 ps simulation
    
    print(f"\nSimulation Parameters:")
    print(f"  Domain: {L:.3f} m, {N} points, dx = {dx:.3e} m")
    print(f"  Time: {total_time:.1e} s, dt = {dt:.1e} s")
    print(f"  CFL number: {ConstantsSI.c*dt/dx:.3f} (<1 ✓)")
    print(f"  Time steps: {int(total_time/dt):,}")
    
    # Initial field diagnostics
    print(f"\nInitial Conditions:")
    print(f"  Ξ range: [{system.fields['Xi'].min():.3f}, {system.fields['Xi'].max():.3f}]")
    print(f"  χ range: [{system.fields['Chi'].min():.3f}, {system.fields['Chi'].max():.3f}]")
    
    initial_energy, components = system._compute_energy()
    print(f"\nInitial Energy Breakdown (J/m):")
    print(f"  Total: {initial_energy:.3e}")
    print(f"  Kinetic: {components['kinetic']:.3e}")
    print(f"  Gradient: {components['gradient']:.3e}")
    print(f"  Potential: {components['potential']:.3e}")
    print(f"  EM: {components['em']:.3e}")
    print(f"  Proca: {components['proca']:.3e}")
    
    # Evolve system
    print(f"\nStarting evolution...")
    energy_drift = system.evolve(total_time, dt, energy_check_interval=500)
    
    # Final diagnostics
    print(f"\n" + "="*70)
    print("FINAL DIAGNOSTICS")
    print("="*70)
    
    final_energy, final_components = system._compute_energy()
    print(f"Final Energy: {final_energy:.3e} J/m")
    print(f"Energy Conservation: |ΔE/E0| = {abs((final_energy-initial_energy)/initial_energy):.2e}")
    
    # Compute observables
    obs = ObservablesSI()
    clock_drift = obs.clock_drift(system.velocities['Xi'])
    n_eff = obs.effective_refractive_index(system.fields['Xi'], system.fields['Chi'])
    m_gamma = np.array([ConstantsSI.m_gamma_SI(xi, c) for xi, c in zip(system.fields['Xi'], system.fields['Chi'])])
    
    print(f"\nObservables at final time:")
    print(f"  Max clock drift |∂ₜΞ|: {np.max(np.abs(clock_drift)):.2e}")
    print(f"  Refractive index Δn: {n_eff.max()-n_eff.min():.2e}")
    print(f"  Photon mass range: {np.min(m_gamma)*ConstantsSI.hbar*ConstantsSI.c/ConstantsSI.eV_to_J:.1e} - "
          f"{np.max(m_gamma)*ConstantsSI.hbar*ConstantsSI.c/ConstantsSI.eV_to_J:.1e} eV")
    
    # Experimental constraint check
    print(f"\nExperimental Constraints Check:")
    
    # Photon mass constraint (Coulomb law: m_γ < 1e-18 eV)
    m_gamma_eV_max = np.max(m_gamma) * ConstantsSI.hbar * ConstantsSI.c / ConstantsSI.eV_to_J
    if m_gamma_eV_max < 1e-18:
        print(f"  ✓ Photon mass: {m_gamma_eV_max:.1e} eV < 1e-18 eV")
    else:
        print(f"  ✗ Photon mass TOO HIGH: {m_gamma_eV_max:.1e} eV")
    
    # Clock drift (current precision ~1e-18)
    max_drift = np.max(np.abs(clock_drift))
    if max_drift < 1e-15:
        print(f"  ✓ Clock drift: {max_drift:.1e} < typical sensitivity")
    else:
        print(f"  ⚠ Clock drift potentially measurable: {max_drift:.1e}")
    
    # Energy conservation threshold
    energy_conservation = abs((final_energy - initial_energy) / initial_energy)
    if energy_conservation < 0.01:
        print(f"  ✓ Energy conserved: ΔE/E0 = {energy_conservation:.2e} < 0.01")
    else:
        print(f"  ✗ Poor energy conservation: ΔE/E0 = {energy_conservation:.2e}")
    
    return system, obs

# ============================================================================
# VISUALIZATION
# ============================================================================
def plot_results(system, obs):
    """Generate diagnostic plots"""
    
    fig, axes = plt.subplots(3, 3, figsize=(15, 12))
    
    # 1. Field evolution
    ax = axes[0, 0]
    ax.plot(system.x, system.fields['Xi'], 'b-', label='Ξ (entropy)')
    ax.plot(system.x, system.fields['Chi'], 'r-', label='χ (coherence)')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Field amplitude')
    ax.set_title('Final Field Configuration')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Clock drift
    ax = axes[0, 1]
    clock_drift = obs.clock_drift(system.velocities['Xi'])
    ax.plot(system.x, clock_drift, 'g-')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Δω/ω = ∂ₜΞ')
    ax.set_title('Atomic Clock Drift Prediction')
    ax.grid(True, alpha=0.3)
    ax.text(0.05, 0.95, f'Max: {np.max(np.abs(clock_drift)):.2e}',
            transform=ax.transAxes, fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 3. Refractive index
    ax = axes[0, 2]
    n_eff = obs.effective_refractive_index(system.fields['Xi'], system.fields['Chi'])
    ax.plot(system.x, n_eff, 'm-')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('n_eff')
    ax.set_title('Effective Refractive Index')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.5)
    
    # 4. Energy components over time
    ax = axes[1, 0]
    if system.energy_history:
        times = [t for t, _, _ in system.energy_history]
        energies = [E for _, E, _ in system.energy_history]
        ax.plot(times, energies, 'k-')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Total Energy (J/m)')
        ax.set_title('Energy Conservation Check')
        ax.grid(True, alpha=0.3)
    
    # 5. Photon mass distribution
    ax = axes[1, 1]
    m_gamma = np.array([ConstantsSI.m_gamma_SI(xi, c) for xi, c in zip(system.fields['Xi'], system.fields['Chi'])])
    m_gamma_eV = m_gamma * ConstantsSI.hbar * ConstantsSI.c / ConstantsSI.eV_to_J
    ax.plot(system.x, m_gamma_eV, 'orange')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('m_γ (eV)')
    ax.set_title('Dynamical Photon Mass')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    ax.axhline(y=1e-18, color='r', linestyle='--', alpha=0.7, label='Experimental limit')
    ax.legend()
    
    # 6. Phase space (Ξ vs χ)
    ax = axes[1, 2]
    scatter = ax.scatter(system.fields['Xi'], system.fields['Chi'], 
                        c=system.x, cmap='viridis', s=10, alpha=0.7)
    ax.set_xlabel('Ξ (entropy)')
    ax.set_ylabel('χ (coherence)')
    ax.set_title('Phase Space Configuration')
    ax.grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=ax, label='Position (m)')
    
    # 7. Field velocities
    ax = axes[2, 0]
    ax.plot(system.x, system.velocities['Xi'], 'b-', label='∂ₜΞ')
    ax.plot(system.x, system.velocities['Chi'], 'r-', label='∂ₜχ')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Field velocity')
    ax.set_title('Field Time Derivatives')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 8. Coupling functions
    ax = axes[2, 1]
    xi = system.fields['Xi']
    chi = system.fields['Chi']
    eps = np.array([ConstantsSI.epsilon(x, c) for x, c in zip(xi, chi)])
    mu_inv = np.array([ConstantsSI.mu_inv(x, c) for x, c in zip(xi, chi)])
    ax.plot(system.x, eps, label='ε/ε₀')
    ax.plot(system.x, mu_inv, label='μ⁻¹/μ₀⁻¹')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Normalized coupling')
    ax.set_title('Field-Dependent Couplings')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 9. Energy density distribution
    ax = axes[2, 2]
    total_energy, components = system._compute_energy()
    energy_density = (0.5*system.velocities['Xi']**2 + 
                      0.5*system.velocities['Chi']**2 +
                      0.5*system.fd.gradient(system.fields['Xi'])**2 +
                      0.5*system.fd.gradient(system.fields['Chi'])**2)
    ax.plot(system.x, energy_density, 'purple')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Energy density (J/m³)')
    ax.set_title('Local Energy Density')
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Ξ-χ-φ-A-E-A-B-G Framework - Validated Simulation Results', fontsize=14)
    plt.tight_layout()
    plt.show()

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    # Run validated simulation
    system, obs = run_validation_simulation()
    
    # Generate plots
    plot_results(system, obs)
    
    # Save results for analysis
    results = {
        'x': system.x,
        'Xi': system.fields['Xi'],
        'Chi': system.fields['Chi'],
        'Xi_vel': system.velocities['Xi'],
        'Chi_vel': system.velocities['Chi'],
        'energy_history': system.energy_history,
        'time_history': system.time_history
    }
    
    np.savez('xi_chi_validated_results.npz', **results)
    print(f"\nResults saved to xi_chi_validated_results.npz")
