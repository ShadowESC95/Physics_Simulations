# Inside handler():
telemetry = {
    "frame": current_step,
    "drift": np.mean(drift_tensor),
    "entropy": np.load("output/xi_entropy_log.npy")[-1]
}

# Replace static data with:
telemetry = {
    "frame": step,
    "drift": np.load("output/drift_tensor_Xi.npy")[step].mean(),
    "entropy": np.load("output/xi_entropy_log.npy")[step]
}
