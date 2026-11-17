
import numpy as np
from lagrangian import (
    eps_func, mu_inv_func, m_gamma, V_potential, dV_dXi, dV_dchi,
    deps_dXi, deps_dchi, dmuinv_dXi, dmuinv_dchi, dm2_dXi, dm2_dchi, energy_density
)

def laplacian_1d(field, dx):
    return (np.roll(field, -1) - 2.0*field + np.roll(field, 1)) / (dx*dx)

def gradient_1d(field, dx):
    return (np.roll(field, -1) - np.roll(field, 1)) / (2.0*dx)

def rk4_step(state, dt, dx, p):
    def accel(s):
        Xi, chi, AE, AB = s['Xi'], s['chi'], s['AE'], s['AB']
        dXi, dchi, dAE, dAB = s['dXi'], s['dchi'], s['dAE'], s['dAB']

        Xix = gradient_1d(Xi, dx); chix = gradient_1d(chi, dx)
        AEx = gradient_1d(AE, dx); ABx = gradient_1d(AB, dx)

        Xixx = laplacian_1d(Xi, dx); chixx = laplacian_1d(chi, dx)
        AExx = laplacian_1d(AE, dx); ABxx = laplacian_1d(AB, dx)

        eps  = eps_func(Xi, chi, p)
        muI  = mu_inv_func(Xi, chi, p)
        m2   = m_gamma(Xi, chi, p)**2

        deps_dt = deps_dXi(Xi, chi, p)*dXi + deps_dchi(Xi, chi, p)*dchi

        d2AE = (muI*AExx - m2*AE - deps_dt*dAE) / (eps + 1e-12)
        d2AB = (muI*ABxx - m2*AB - deps_dt*dAB) / (eps + 1e-12)

        d2Xi = (
    p['c_Xi']**2 * Xixx - dV_dXi(Xi, chi, p)
    - 0.5*deps_dXi(Xi, chi, p)*(dAE**2 + dAB**2)
    + 0.5*dmuinv_dXi(Xi, chi, p)*(AEx**2 + ABx**2)
    - 0.5*dm2_dXi(Xi, chi, p)*(AE**2 + AB**2)
)

        d2chi = (
    p['c_chi']**2 * chixx - dV_dchi(Xi, chi, p)
    - 0.5*deps_dchi(Xi, chi, p)*(dAE**2 + dAB**2)
    + 0.5*dmuinv_dchi(Xi, chi, p)*(AEx**2 + ABx**2)
    - 0.5*dm2_dchi(Xi, chi, p)*(AE**2 + AB**2)
)

        return dict(dXi=d2Xi, dchi=d2chi, dAE=d2AE, dAB=d2AB)

    # RK4
    k1v = accel(state)
    k1f = dict(Xi=state['dXi'], chi=state['dchi'], AE=state['dAE'], AB=state['dAB'])

    s2 = {k:(state[k] + 0.5*dt*k1f.get(k,0)) for k in state}
    for k in ['dXi','dchi','dAE','dAB']:
        s2[k] = state[k] + 0.5*dt*k1v[k]
    k2v = accel(s2)
    k2f = dict(Xi=s2['dXi'], chi=s2['dchi'], AE=s2['dAE'], AB=s2['dAB'])

    s3 = {k:(state[k] + 0.5*dt*k2f.get(k,0)) for k in state}
    for k in ['dXi','dchi','dAE','dAB']:
        s3[k] = state[k] + 0.5*dt*k2v[k]
    k3v = accel(s3)
    k3f = dict(Xi=s3['dXi'], chi=s3['dchi'], AE=s3['dAE'], AB=s3['dAB'])

    s4 = {k:(state[k] + dt*k3f.get(k,0)) for k in state}
    for k in ['dXi','dchi','dAE','dAB']:
        s4[k] = state[k] + dt*k3v[k]
    k4v = accel(s4)
    k4f = dict(Xi=s4['dXi'], chi=s4['dchi'], AE=s4['dAE'], AB=s4['dAB'])

    new = {}
    for fld in ['Xi','chi','AE','AB']:
        new[fld]  = state[fld]  + (dt/6.0)*(k1f[fld] + 2*k2f[fld] + 2*k3f[fld] + k4f[fld])
    for vel in ['dXi','dchi','dAE','dAB']:
        new[vel] = state[vel] + (dt/6.0)*(k1v[vel] + 2*k2v[vel] + 2*k3v[vel] + k4v[vel])

    return new

def run_sim(params, out_callback=None):
    nx = params['nx']; Lx = params['Lx']; dt = params['dt']; steps = params['steps']
    dx = Lx/nx
    x  = np.linspace(0, Lx, nx, endpoint=False)

    Xi0 = params['V_params']['Xi0']; chi0 = params['V_params']['chi0']
    Xi  = Xi0 + params['init']['Xi_amp']*np.sin(params['init']['Xi_k']*x)
    chi = chi0 + params['init']['chi_amp']*np.sin(params['init']['chi_k']*x)

    def gauss(a, x0, sig): return a*np.exp(-0.5*((x-x0)/sig)**2)
    AE  = gauss(params['init']['A_E_amp'], params['init']['A_E_x0'], params['init']['A_E_sigma'])
    AB  = gauss(params['init']['A_B_amp'], params['init']['A_B_x0'], params['init']['A_B_sigma'])

    state = dict(Xi=Xi, chi=chi, AE=AE, AB=AB,
                 dXi=np.zeros(nx), dchi=np.zeros(nx),
                 dAE=np.zeros(nx), dAB=np.zeros(nx))

    energies = []
    for n in range(steps+1):
        Xix = gradient_1d(state['Xi'], dx); chix = gradient_1d(state['chi'], dx)
        AEx = gradient_1d(state['AE'], dx); ABx = gradient_1d(state['AB'], dx)

        H = energy_density(state['Xi'], state['chi'], state['AE'], state['AB'],
                           state['dXi'], state['dchi'], state['dAE'], state['dAB'],
                           Xix, chix, AEx, ABx, params)
        energies.append(H.mean())

        if out_callback and (n % params['save_every'] == 0):
            out_callback(n, x, state, H)

        state = rk4_step(state, dt, dx, params)

    return x, state, np.array(energies)
