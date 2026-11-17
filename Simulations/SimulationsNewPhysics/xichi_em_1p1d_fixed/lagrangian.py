
import numpy as np

def eps_func(Xi, chi, p):
    return p['epsilon0'] * (1.0 + p['a_Xi']*(Xi-1.0) + p['a_chi']*(chi-1.0))

def mu_inv_func(Xi, chi, p):
    mu0_inv = 1.0/p['mu0']
    return mu0_inv * (1.0 + p['b_Xi']*(Xi-1.0) + p['b_chi']*(chi-1.0))

def m_gamma(Xi, chi, p):
    return p['epsilon_s'] * np.abs(Xi*chi)

def V_potential(Xi, chi, p):
    lamX = p['V_params']['lambda_Xi']
    lamC = p['V_params']['lambda_chi']
    kap  = p['V_params']['kappa']
    Xi0  = p['V_params']['Xi0']
    chi0 = p['V_params']['chi0']
    return 0.5*lamX*(Xi-Xi0)**2 + 0.5*lamC*(chi-chi0)**2 + kap*(Xi-Xi0)*(chi-chi0)

def dV_dXi(Xi, chi, p):
    lamX = p['V_params']['lambda_Xi']
    kap  = p['V_params']['kappa']
    Xi0  = p['V_params']['Xi0']
    chi0 = p['V_params']['chi0']
    return lamX*(Xi-Xi0) + kap*(chi-chi0)

def dV_dchi(Xi, chi, p):
    lamC = p['V_params']['lambda_chi']
    kap  = p['V_params']['kappa']
    Xi0  = p['V_params']['Xi0']
    chi0 = p['V_params']['chi0']
    return lamC*(chi-chi0) + kap*(Xi-Xi0)

def deps_dXi(Xi, chi, p): return p['epsilon0'] * p['a_Xi']*np.ones_like(Xi)
def deps_dchi(Xi, chi, p): return p['epsilon0'] * p['a_chi']*np.ones_like(Xi)
def dmuinv_dXi(Xi, chi, p): return (1.0/p['mu0']) * p['b_Xi']*np.ones_like(Xi)
def dmuinv_dchi(Xi, chi, p): return (1.0/p['mu0']) * p['b_chi']*np.ones_like(Xi)

def dm2_dXi(Xi, chi, p):
    epss = p['epsilon_s']
    sgn = np.sign(Xi*chi)
    return 2.0 * (p['epsilon_s'] * np.abs(Xi*chi)) * (epss * sgn * chi)

def dm2_dchi(Xi, chi, p):
    epss = p['epsilon_s']
    sgn = np.sign(Xi*chi)
    return 2.0 * (p['epsilon_s'] * np.abs(Xi*chi)) * (epss * sgn * Xi)

def energy_density(Xi, chi, AE, AB, dXi, dchi, dAE, dAB, Xix, chix, AEx, ABx, p):
    eps  = eps_func(Xi, chi, p)
    muI  = mu_inv_func(Xi, chi, p)
    m2   = m_gamma(Xi, chi, p)**2
    H = 0.5*(dXi**2 + p['c_Xi']**2 * Xix**2)       + 0.5*(dchi**2 + p['c_chi']**2 * chix**2)       + 0.5*eps*(dAE**2 + dAB**2)       + 0.5*muI*(AEx**2 + ABx**2)       + 0.5*m2*(AE**2 + AB**2)       + V_potential(Xi, chi, p)
    return H
