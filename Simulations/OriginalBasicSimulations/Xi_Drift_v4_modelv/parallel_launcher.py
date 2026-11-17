# Inside parallel_launcher.py loop:
from engine.anomaly import detect_entropy_anomalies
entropy_series = np.load("output/xi_entropy_log.npy")
anomalies = detect_entropy_anomalies(entropy_series)
logger.log_scalar("Anomalies/Count", len(anomalies), step)
