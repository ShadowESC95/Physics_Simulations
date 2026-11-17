import numpy as np

def christoffel_symbols(metric, dmetric):
    dim = metric.shape[0]
    gamma = np.zeros((dim, dim, dim))
    inv_metric = np.linalg.inv(metric)
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                gamma[i, j, k] = 0.5 * sum(
                    inv_metric[i, l] * (dmetric[l, j, k] + dmetric[l, k, j] - dmetric[j, k, l])
                    for l in range(dim)
                )
    return gamma

def riemann_tensor(gamma, dgamma):
    dim = gamma.shape[0]
    R = np.zeros((dim, dim, dim, dim))
    for rho in range(dim):
        for sigma in range(dim):
            for mu in range(dim):
                for nu in range(dim):
                    R[rho, sigma, mu, nu] = dgamma[rho, sigma, nu] - dgamma[rho, sigma, mu]
                    R[rho, sigma, mu, nu] += sum(
                        gamma[rho, mu, l] * gamma[l, sigma, nu] - gamma[rho, nu, l] * gamma[l, sigma, mu]
                        for l in range(dim)
                    )
    return R

def ricci_tensor(R):
    dim = R.shape[0]
    Ricci = np.zeros((dim, dim))
    for mu in range(dim):
        for nu in range(dim):
            Ricci[mu, nu] = sum(R[rho, mu, rho, nu] for rho in range(dim))
    return Ricci

def ricci_scalar(Ricci, metric):
    return np.sum(metric**-1 * Ricci)

def einstein_tensor(Ricci, R_scalar, metric):
    dim = metric.shape[0]
    G = Ricci - 0.5 * R_scalar * metric
    return G
