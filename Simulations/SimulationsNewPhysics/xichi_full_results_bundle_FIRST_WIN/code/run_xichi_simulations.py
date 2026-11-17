import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

# Define XiChiSolver class inline
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

def run_single_simulation():
    """Run a single simulation with default parameters"""
    print("Running single simulation with default parameters...")
    
    solver = XiChiSolver()
    solver.coupling_method = "potential"
    
    # Initial conditions: [Xi, chi, Xi_dot, chi_dot]
    initial_conditions = [1.0, 0.5, 0.0, 0.0]
    
    # Solve
    sol = solver.solve(initial_conditions, t_span=(0, 100), n_points=1000)
    
    # Analyze
    results = solver.analyze_solution(sol)
    
    # Print results
    print("\n=== Simulation Results ===")
    for key, value in results.items():
        print(f"{key}: {value}")
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Xi and chi evolution
    axes[0, 0].plot(sol.t, sol.y[0], label='Ξ (Entropy)', linewidth=2)
    axes[0, 0].plot(sol.t, sol.y[1], label='χ (Coherence)', linewidth=2)
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('Field Value')
    axes[0, 0].set_title('Field Evolution')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Field velocities
    axes[0, 1].plot(sol.t, sol.y[2], label='dΞ/dt', linewidth=2)
    axes[0, 1].plot(sol.t, sol.y[3], label='dχ/dt', linewidth=2)
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('Field Velocity')
    axes[0, 1].set_title('Field Velocities')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Phase space: Xi vs chi
    axes[1, 0].plot(sol.y[0], sol.y[1], linewidth=2, alpha=0.7)
    axes[1, 0].scatter(sol.y[0][0], sol.y[1][0], c='green', s=100, label='Start', zorder=5)
    axes[1, 0].scatter(sol.y[0][-1], sol.y[1][-1], c='red', s=100, label='End', zorder=5)
    axes[1, 0].set_xlabel('Ξ (Entropy)')
    axes[1, 0].set_ylabel('χ (Coherence)')
    axes[1, 0].set_title('Phase Space Trajectory')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Energy evolution
    V = np.array([solver.potential_original(sol.y[0][i], sol.y[1][i]) for i in range(len(sol.t))])
    KE = 0.5 * (sol.y[2]**2 + sol.y[3]**2)
    E_total = V + KE
    
    axes[1, 1].plot(sol.t, V, label='Potential', linewidth=2)
    axes[1, 1].plot(sol.t, KE, label='Kinetic', linewidth=2)
    axes[1, 1].plot(sol.t, E_total, label='Total', linewidth=2, linestyle='--')
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Energy')
    axes[1, 1].set_title('Energy Evolution')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('xichi_single_simulation.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved as 'xichi_single_simulation.png'")
    plt.show()
    
    return sol, results

def run_epsilon_sweep():
    """Sweep over epsilon values"""
    print("\nRunning epsilon sweep...")
    
    epsilon_values = np.logspace(-6, -3, 20)  # 1e-6 to 1e-3
    results_list = []
    
    initial_conditions = [1.0, 0.5, 0.0, 0.0]
    
    for eps in tqdm(epsilon_values, desc="Epsilon sweep"):
        solver = XiChiSolver()
        solver.epsilon = eps
        solver.coupling_method = "potential"
        
        sol = solver.solve(initial_conditions, t_span=(0, 100), n_points=500)
        results = solver.analyze_solution(sol)
        results_list.append(results)
    
    df = pd.DataFrame(results_list)
    
    # Plot results
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].semilogx(df['epsilon'], df['xi_final'], 'o-', linewidth=2)
    axes[0, 0].set_xlabel('ε (Stueckelberg coupling)')
    axes[0, 0].set_ylabel('Final Ξ')
    axes[0, 0].set_title('Final Entropy vs ε')
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].semilogx(df['epsilon'], df['chi_final'], 'o-', linewidth=2, color='orange')
    axes[0, 1].set_xlabel('ε (Stueckelberg coupling)')
    axes[0, 1].set_ylabel('Final χ')
    axes[0, 1].set_title('Final Coherence vs ε')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].loglog(df['epsilon'], df['m_gamma'], 'o-', linewidth=2, color='green')
    axes[1, 0].set_xlabel('ε (Stueckelberg coupling)')
    axes[1, 0].set_ylabel('Photon Mass mγ')
    axes[1, 0].set_title('Emergent Photon Mass vs ε')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].semilogx(df['epsilon'], df['E_drop'], 'o-', linewidth=2, color='red')
    axes[1, 1].set_xlabel('ε (Stueckelberg coupling)')
    axes[1, 1].set_ylabel('Energy Drop')
    axes[1, 1].set_title('Energy Dissipation vs ε')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('xichi_epsilon_sweep.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved as 'xichi_epsilon_sweep.png'")
    plt.show()
    
    # Save data
    df.to_csv('epsilon_sweep_results.csv', index=False)
    print("Data saved as 'epsilon_sweep_results.csv'")
    
    return df

def compare_coupling_methods():
    """Compare different coupling methods"""
    print("\nComparing coupling methods...")
    
    methods = ["potential", "photon_feedback", "damping"]
    initial_conditions = [1.0, 0.5, 0.0, 0.0]
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    for method in methods:
        solver = XiChiSolver()
        solver.coupling_method = method
        solver.epsilon = 1e-4
        
        sol = solver.solve(initial_conditions, t_span=(0, 100), n_points=1000)
        
        axes[0, 0].plot(sol.t, sol.y[0], label=f'{method}', linewidth=2)
        axes[0, 1].plot(sol.t, sol.y[1], label=f'{method}', linewidth=2)
        axes[1, 0].plot(sol.y[0], sol.y[1], label=f'{method}', linewidth=2, alpha=0.7)
        
        # Energy
        V = np.array([solver.potential_original(sol.y[0][i], sol.y[1][i]) for i in range(len(sol.t))])
        KE = 0.5 * (sol.y[2]**2 + sol.y[3]**2)
        E_total = V + KE
        axes[1, 1].plot(sol.t, E_total, label=f'{method}', linewidth=2)
    
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('Ξ (Entropy)')
    axes[0, 0].set_title('Entropy Field Evolution')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('χ (Coherence)')
    axes[0, 1].set_title('Coherence Field Evolution')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].set_xlabel('Ξ (Entropy)')
    axes[1, 0].set_ylabel('χ (Coherence)')
    axes[1, 0].set_title('Phase Space Comparison')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].set_xlabel('Time')
    axes[1, 1].set_ylabel('Total Energy')
    axes[1, 1].set_title('Energy Evolution Comparison')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('xichi_coupling_comparison.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved as 'xichi_coupling_comparison.png'")
    plt.show()

if __name__ == "__main__":
    print("=" * 60)
    print("Xi-Chi Field Dynamics Simulation")
    print("=" * 60)
    
    # Run single simulation
    sol, results = run_single_simulation()
    
    # Run epsilon sweep
    df_sweep = run_epsilon_sweep()
    
    # Compare coupling methods
    compare_coupling_methods()
    
    print("\n" + "=" * 60)
    print("All simulations complete!")
    print("=" * 60)
