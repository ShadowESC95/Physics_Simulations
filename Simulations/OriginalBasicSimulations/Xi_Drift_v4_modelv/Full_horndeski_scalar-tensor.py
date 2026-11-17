# Define a symbolic prototype for Model 5: Full Horndeski Extension

from sympy import symbols, Function, diff, simplify

# Define symbolic fields and derivatives
t, x, y, z = symbols('t x y z')
Xi = Function('Xi')(t, x, y, z)
X = Function('X')(t, x, y, z)  # Kinetic term: X = 1/2 ∂μΞ ∂^μΞ
R = Function('R')(t, x, y, z)  # Ricci scalar (proxy: ∇²χ)

# Define Horndeski functions
G2 = Function('G2')(Xi, X)
G3 = Function('G3')(Xi, X)
G4 = Function('G4')(Xi)
G5 = Function('G5')(Xi)

# Prototype Lagrangian terms
L2 = G2
L3 = -G3 * diff(Xi, t)
L4 = G4 * R  # Plus derivative terms omitted here
L5 = -G5 * R * diff(Xi, t)  # Simplified variant

# Full prototype Horndeski Lagrangian (symbolic)
L_Horndeski = L2 + L3 + L4 + L5
L_Horndeski_simplified = simplify(L_Horndeski)

L_Horndeski_simplified
