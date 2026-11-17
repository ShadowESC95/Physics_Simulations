import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load simulation outputs (merged from ranks)
def load_field_sequence(folder="output/", steps=100, prefix="xi"):
    data = []
    for step in range(steps):
        for rank in range(4):  # Adjust to match your MPI count
            path = f"{folder}/{prefix}_step_{rank}_{step}.npy"
            try:
                arr = np.load(path).flatten()
                data.append(arr)
            except:
                continue
    return np.array(data)

xi_seq = load_field_sequence(prefix="xi")
chi_seq = load_field_sequence(prefix="chi")
combined = np.hstack((xi_seq, chi_seq))

# Normalize and reduce
scaler = StandardScaler()
scaled = scaler.fit_transform(combined)

pca = PCA(n_components=3)
reduced = pca.fit_transform(scaled)

# Clustering
kmeans = KMeans(n_clusters=3)
labels = kmeans.fit_predict(reduced)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(reduced[:,0], reduced[:,1], reduced[:,2], c=labels, cmap="plasma", s=2)
ax.set_title("Ξχ Phase Stability Clustering")
plt.savefig("plots/xi_chi_phase_clusters.png", dpi=300)
