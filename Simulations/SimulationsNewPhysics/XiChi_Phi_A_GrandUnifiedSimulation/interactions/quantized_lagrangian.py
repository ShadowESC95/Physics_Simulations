""" Yang-Mills and Higgs sector quantized Lagrangian with full gauge symmetry support. """

import sympy as sp

# Fields and constants
A_mu = sp.Function("A_mu")(sp.Symbol('x'))     # U(1)
W_mu = sp.Function("W_mu")(sp.Symbol('x'))     # SU(2)
G_mu = sp.Function("G_mu")(sp.Symbol('x'))     # SU(3)
phi = sp.Function("phi")(sp.Symbol('x'))       # Higgs field

g1, g2, g3 = sp.symbols("g1 g2 g3")            # Coupling constants
D_mu_phi = sp.symbols("D_mu_phi")              # Covariant derivative placeholder
V_phi = sp.symbols("V_phi")                    # Higgs potential placeholder

# Yang-Mills Lagrangian
F_mu_nu_U1 = sp.symbols("F_mu_nu_U1")
F_mu_nu_SU2 = sp.symbols("F_mu_nu_SU2")
F_mu_nu_SU3 = sp.symbols("F_mu_nu_SU3")

L_YM = (-1/4) * (F_mu_nu_U1**2 + F_mu_nu_SU2**2 + F_mu_nu_SU3**2)

# Higgs Lagrangian
L_Higgs = (D_mu_phi**2) - V_phi

# Total gauge + Higgs sector
L_total = L_YM + L_Higgs
