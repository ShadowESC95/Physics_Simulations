import numpy as np

def mutual_information_entropy(chi_field):
    """
    Approximates coherence by computing pairwise mutual information-like decay.

    Args:
        chi_field (np.ndarray): χ(x, y, z, t) field over space-time

    Returns:
        float: Scalar coherence metric (lower means more decoherence)
    """
    # Flatten spatial dimensions, average over time
    chi_flat = chi_field.reshape(-1, chi_field.shape[-1])
    mean = np.mean(chi_flat, axis=0)
    var = np.var(chi_flat, axis=0)
    entropy = -np.sum(mean * np.log(np.clip(mean, 1e-10, None)))

    # Mutual coherence proxy
    normalized_chi = (chi_flat - mean) / (np.sqrt(var) + 1e-10)
    correlation = np.mean(np.dot(normalized_chi, normalized_chi.T))
    coherence_metric = entropy / (correlation + 1e-10)

    return coherence_metric

