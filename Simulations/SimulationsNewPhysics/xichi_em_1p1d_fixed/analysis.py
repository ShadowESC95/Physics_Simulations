
import numpy as np
import matplotlib.pyplot as plt
from lagrangian import eps_func, mu_inv_func

def phase_velocity_avg(Xi, chi, params):
    eps = eps_func(Xi, chi, params).mean()
    mu_inv = mu_inv_func(Xi, chi, params).mean()
    v = np.sqrt(mu_inv/(eps + 1e-15))
    return float(v)

def track_pulse_speed(x, field_t0, field_t1, dt):
    i0 = np.argmax(field_t0)
    i1 = np.argmax(field_t1)
    dx = x[1]-x[0]
    shift = (i1 - i0)*dx
    return float(shift/dt)
