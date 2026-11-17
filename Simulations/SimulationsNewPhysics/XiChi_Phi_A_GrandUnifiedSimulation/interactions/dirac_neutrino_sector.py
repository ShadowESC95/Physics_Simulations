""" Dirac and neutrino Lagrangian sector with chiral spinor terms. """

import sympy as sp

# Dirac spinors and mass terms
psi = sp.Function("psi")(sp.Symbol('x'))  # electron
nu = sp.Function("nu")(sp.Symbol('x'))    # neutrino
m_psi, m_nu = sp.symbols("m_psi m_nu")

# Dirac equation structure
L_dirac = sp.I * sp.symbols("bar_psi") * sp.symbols("gamma_mu") * sp.symbols("partial_mu_psi") - m_psi * sp.symbols("bar_psi") * psi
L_neutrino = sp.I * sp.symbols("bar_nu") * sp.symbols("gamma_mu") * sp.symbols("partial_mu_nu") - m_nu * sp.symbols("bar_nu") * nu

L_total_dirac = L_dirac + L_neutrino
