import sympy as sp

# === Symbolic spacetime variables ===
t, x, y, z = sp.symbols('t x y z')
coords = (t, x, y, z)

# === Scalar fields ===
Xi = sp.Function('Xi')(*coords)
chi = sp.Function('chi')(*coords)
phi = sp.Function('phi')(*coords)

# === Vector field Aμ ===
A = [sp.Function(f'A{i}')(*coords) for i in range(4)]

# === Constants ===
alpha, beta = sp.symbols('alpha beta')
m_Xi, m_chi, m_phi = sp.symbols('m_Xi m_chi m_phi')
m_A = sp.symbols('m_A')  # For Stueckelberg term

# === Derivatives ===
d_Xi = [sp.diff(Xi, v) for v in coords]
d_chi = [sp.diff(chi, v) for v in coords]
d_phi = [sp.diff(phi, v) for v in coords]

# === Field strength tensor Fμν ===
F = [[sp.diff(A[i], coords[j]) - sp.diff(A[j], coords[i]) for j in range(4)] for i in range(4)]

# === Lagrangian terms ===
L_Xi = 0.5 * sum(d**2 for d in d_Xi) - 0.5 * m_Xi**2 * Xi**2
L_chi = 0.5 * sum(d**2 for d in d_chi) - 0.5 * m_chi**2 * chi**2
L_phi = 0.5 * sum(d**2 for d in d_phi) - 0.5 * m_phi**2 * phi**2
L_EM = -0.25 * sum(F[i][j]**2 for i in range(4) for j in range(i + 1, 4))

# === Stueckelberg mass term: (Aμ - ∂μφ)^2 ===
L_Stueckelberg = 0.5 * m_A**2 * sum((A[i] - d_phi[i])**2 for i in range(4))

# === Interaction: coherence–entropy coupling ===
L_int = -alpha * chi * Xi - beta * Xi**2 * chi**2

# === Total Lagrangian ===
L_total = L_Xi + L_chi + L_phi + L_EM + L_Stueckelberg + L_int

# === Fields to vary ===
fields = {
    "Xi": Xi,
    "chi": chi,
    "phi": phi,
}
fields.update({f"A{i}": A[i] for i in range(4)})

# === Euler–Lagrange equations ===
EL_equations = {}

for name, field in fields.items():
    dL_df = sp.diff(L_total, field)
    dL_ddf = [sp.diff(L_total, sp.diff(field, v)) for v in coords]
    div_term = sum(sp.diff(dL_ddf[i], coords[i]) for i in range(4))
    EL_equations[name] = sp.simplify(dL_df - div_term)

# === EXPORT FUNCTIONS ===
def get_field_equations(fields_dict=None, config=None):
    return EL_equations

def get_lagrangian():
    return L_total

