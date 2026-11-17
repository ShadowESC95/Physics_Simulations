import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

class XiChiSolver:
    def __init__(self):
        # Core parameters - SWEEP THESE
        self.epsilon = 1e-5      # Stueckelberg coupling - NOW USED!
        self.lambda_pot = 1.0    # Potential strength  
        self.Gamma = 1.0         # Coherence threshold
        self.delta = 0.01        # Smoothing parameter
        
        # Numerical parameters
        self.H = 0.01           # Hubble damping
        self.k = 0.1            # Wavevector
        
        # Coupling method (choose one)
        self.coupling_method = "potential"  # "potential", "photon_feedback", "damping"
        
    def potential_original(self, Xi, chi):
        """Original smooth potential from FINAL.pdf"""
        return self.lambda_pot * ((Xi * chi - self.Gamma)**2 + self.delta**2)**2
    
    def potential_gradient_original(self, Xi, chi):
        """Original gradient without epsilon coupling"""
        common = 4 * self.lambda_pot * (Xi * chi - self.Gamma) * ((Xi * chi - self.Gamma)**2 + self.delta**2)
        dV_dXi = common * chi
        dV_dchi = common * Xi
        return dV_dXi, dV_dchi
    
    def potential_with_epsilon(self, Xi, chi):
        """OPTION 1: Couple ε directly to coherence threshold"""
        # ε modulates the coherence scale - PHYSICALLY MOTIVATED
        effective_Gamma = self.Gamma * (1 + self.epsilon * Xi * chi)
        return self.lambda_pot * ((Xi * chi - effective_Gamma)**2 + self.delta**2)**2
    
    def potential_gradient_with_epsilon(self, Xi, chi):
        """Gradient for Option 1 coupling"""
        effective_Gamma = self.Gamma * (1 + self.epsilon * Xi * chi)
        common = 4 * self.lambda_pot * (Xi * chi - effective_Gamma) * ((Xi * chi - effective_Gamma)**2 + self.delta**2)
        
        # Derivatives include ε terms
        dGamma_dXi = self.Gamma * self.epsilon * chi
        dGamma_dchi = self.Gamma * self.epsilon * Xi
        
        dV_dXi = common * (chi - dGamma_dXi)
        dV_dchi = common * (Xi - dGamma_dchi)
        
        return dV_dXi, dV_dchi
    
    def photon_mass_feedback(self, Xi, chi):
        """OPTION 2: Photon mass energy density feedback"""
        m_gamma = self.epsilon * Xi * chi
        rho_gamma = 0.5 * m_gamma**2  # Energy in photon mass field
        return rho_gamma
    
    def field_equations_original(self, t, y):
        """Original equations without epsilon coupling"""
        Xi, chi, Xi_dot, chi_dot = y
        dV_dXi, dV_dchi = self.potential_gradient_original(Xi, chi)
        
        Xi_ddot = -3*self.H*Xi_dot - dV_dXi - self.k**2*Xi
        chi_ddot = -3*self.H*chi_dot - dV_dchi - self.k**2*chi
        
        return [Xi_dot, chi_dot, Xi_ddot, chi_ddot]
    
    def field_equations_potential_coupling(self, t, y):
        """OPTION 1: ε couples through potential"""
        Xi, chi, Xi_dot, chi_dot = y
        dV_dXi, dV_dchi = self.potential_gradient_with_epsilon(Xi, chi)
        
        Xi_ddot = -3*self.H*Xi_dot - dV_dXi - self.k**2*Xi
        chi_ddot = -3*self.H*chi_dot - dV_dchi - self.k**2*chi
        
        return [Xi_dot, chi_dot, Xi_ddot, chi_ddot]
    
    def field_equations_photon_feedback(self, t, y):
        """OPTION 2: ε couples through photon mass feedback"""
        Xi, chi, Xi_dot, chi_dot = y
        
        # Original potential gradient
        dV_dXi, dV_dchi = self.potential_gradient_original(Xi, chi)
        
        # Photon mass feedback terms
        m_gamma = self.epsilon * Xi * chi
        rho_gamma = 0.5 * m_gamma**2
        
        # Add photon mass derivatives to potential gradient
        dV_dXi += self.epsilon**2 * Xi * chi**2
        dV_dchi += self.epsilon**2 * Xi**2 * chi
        
        Xi_ddot = -3*self.H*Xi_dot - dV_dXi - self.k**2*Xi
        chi_ddot = -3*self.H*chi_dot - dV_dchi - self.k**2*chi
        
        return [Xi_dot, chi_dot, Xi_ddot, chi_ddot]
    
    def field_equations_damping_coupling(self, t, y):
        """OPTION 3: ε couples through damping terms"""
        Xi, chi, Xi_dot, chi_dot = y
        
        dV_dXi, dV_dchi = self.potential_gradient_original(Xi, chi)
        
        # ε-dependent effective masses and damping
        m_Xi_eff = 1.0 + self.epsilon * chi**2
        m_chi_eff = 1.0 + self.epsilon * Xi**2
        gamma_eff = 0.1 * (1 + self.epsilon * Xi * chi)
        
        Xi_ddot = -3*self.H*Xi_dot - gamma_eff * Xi_dot - m_Xi_eff * dV_dXi - self.k**2*Xi
        chi_ddot = -3*self.H*chi_dot - gamma_eff * chi_dot - m_chi_eff * dV_dchi - self.k**2*chi
        
        return [Xi_dot, chi_dot, Xi_ddot, chi_ddot]
    
    def get_field_equations(self):
        """Select the coupling method"""
        if self.coupling_method == "potential":
            return self.field_equations_potential_coupling
        elif self.coupling_method == "photon_feedback":
            return self.field_equations_photon_feedback
        elif self.coupling_method == "damping":
            return self.field_equations_damping_coupling
        else:
            return self.field_equations_original
    
    def solve(self, initial_conditions, t_span=(0, 100), n_points=1000):
        """Solve the field equations"""
        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        field_eq = self.get_field_equations()
        
        solution = solve_ivp(field_eq, t_span, initial_conditions, 
                           t_eval=t_eval, method='RK45', rtol=1e-8)
        return solution
    
    def analyze_solution(self, sol):
        """Analyze simulation results"""
        Xi_final, chi_final = sol.y[0][-1], sol.y[1][-1]
        Xi_amp, chi_amp = np.max(np.abs(sol.y[0])), np.max(np.abs(sol.y[1]))
        
        # Calculate energies
        V_initial = self.potential_original(sol.y[0][0], sol.y[1][0])
        V_final = self.potential_original(Xi_final, chi_final)
        
        kinetic_initial = 0.5 * (sol.y[2][0]**2 + sol.y[3][0]**2)
        kinetic_final = 0.5 * (sol.y[2][-1]**2 + sol.y[3][-1]**2)
        
        E_initial = V_initial + kinetic_initial
        E_final = V_final + kinetic_final
        E_drop = E_initial - E_final
        
        # Photon mass
        m_gamma = self.epsilon * Xi_final * chi_final
        
        return {
            'epsilon': self.epsilon,
            'lambda_pot': self.lambda_pot,
            'Gamma': self.Gamma,
            'xi_amp': Xi_amp,
            'chi_amp': chi_amp,
            'xi_final': Xi_final,
            'chi_final': chi_final,
            'product': Xi_final * chi_final,
            'V_peak': V_initial,
            'V_final': V_final,
            'E_drop': E_drop,
            'm_gamma': m_gamma,
            'coupling_method': self.coupling_method
        }

# End of user-provided code
