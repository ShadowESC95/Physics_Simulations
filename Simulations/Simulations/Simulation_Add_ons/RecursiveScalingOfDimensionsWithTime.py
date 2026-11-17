import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def recursive_time_scale(time, dimensions, scale_factor=0.9):
    scaled_time = [time]
    for _ in range(dimensions - 1):
        time = time * scale_factor
        scaled_time.append(time)
    return np.array(scaled_time)

# Parameters
initial_time = np.linspace(0, 10, 100)
dimensions = 11
theta = np.linspace(0, 4*np.pi, 100)  # Angular coordinate for spiral

# Recursive scaling
time_matrix = recursive_time_scale(initial_time, dimensions)

# Create figure with specific size and layout
fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection='3d')

# Generate the accretion disk effect
for i in range(dimensions):
    # Calculate radius and height
    radius = 1 + i * 0.5  # Increasing radius for each dimension
    height = (dimensions - i) * 0.2  # Decreasing height for each dimension
    
    # Create spiral coordinates
    x = radius * np.cos(theta + i * np.pi/6)
    y = radius * np.sin(theta + i * np.pi/6)
    z = height + time_matrix[i, :] * 0.1  # Scale the height variation
    
    # Plot the spiral with color gradient
    points = ax.plot(x, y, z, 
                    label=f"Dimension {i+1}",
                    linewidth=2,
                    alpha=0.8,
                    color=plt.cm.viridis(i/dimensions))

# Customize the plot
ax.set_title("3D Recursive Time Scaling - Accretion Disk", pad=20)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Scaled Time")

# Set viewing angle
ax.view_init(elev=30, azim=45)

# Add a color bar - Fixed implementation
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, 
                          norm=plt.Normalize(vmin=1, vmax=dimensions))
sm.set_array([])
plt.subplots_adjust(right=0.85)  # Make room for colorbar
cbar_ax = fig.add_axes([0.88, 0.15, 0.03, 0.7])  # [left, bottom, width, height]
fig.colorbar(sm, cax=cbar_ax, label='Dimension')

plt.show()