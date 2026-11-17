# Adjusted code to allow the user to choose a specific frequency within the range of 0 Hz to 900 Hz

# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate entropy, energy, and time dilation for a specific frequency
def calculate_properties(frequency, S0=1, m_consciousness=1e-5, t_0=1, f_max=900):
    # Entropy S(f) = S0 + log(f)  (since we're removing Boltzmann's constant)
    entropy = S0 + np.log(frequency)
    
    # Energy E(f) = 1/2 * m_consciousness * f^2  (simplified for simulation)
    energy = 0.5 * m_consciousness * frequency**2
    
    # Time dilation t(f) = t_0 * (1 + f/f_max)
    time_dilation = t_0 * (1 + frequency / f_max)
    
    return entropy, energy, time_dilation

# Function to plot results for the selected frequency
def plot_properties(frequency):
    entropy, energy, time_dilation = calculate_properties(frequency)
    
    # Plot Entropy, Energy, and Time Dilation
    plt.figure(figsize=(12, 4))
    
    # Entropy Plot
    plt.subplot(1, 3, 1)
    plt.plot(frequency, entropy, marker='o', color='blue')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Entropy (S)")
    plt.title(f"Entropy at {frequency} Hz")
    plt.grid(True)

    # Energy Plot
    plt.subplot(1, 3, 2)
    plt.plot(frequency, energy, marker='o', color='orange')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Energy (J)")
    plt.title(f"Energy at {frequency} Hz")
    plt.grid(True)

    # Time Dilation Plot
    plt.subplot(1, 3, 3)
    plt.plot(frequency, time_dilation, marker='o', color='green')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Time Dilation (t)")
    plt.title(f"Time Dilation at {frequency} Hz")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Example usage: User can input frequency between 0 to 900 Hz
frequency_input = float(input("Enter a frequency between 0 Hz and 900 Hz: "))

# Check if the frequency input is within valid range
if 0 <= frequency_input <= 900:
    plot_properties(frequency_input)
else:
    print("Please enter a frequency within the valid range (0 to 900 Hz).")
