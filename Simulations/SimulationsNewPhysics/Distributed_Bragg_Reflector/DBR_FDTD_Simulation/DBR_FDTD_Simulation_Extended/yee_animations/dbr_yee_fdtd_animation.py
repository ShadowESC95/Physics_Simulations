
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

dx = 1e-9
dt = dx / (2.998e8 * np.sqrt(2))
L = 2000
T = 1200

Ez = np.zeros(L)
Hy = np.zeros(L)
eps_r = np.ones(L)

n1, n2 = 1.45, 2.1
d1, d2 = 100, 100
for i in range(10):
    eps_r[i*(d1+d2):i*(d1+d2)+d1] = n1**2
    eps_r[i*(d1+d2)+d1:i*(d1+d2)+d1+d2] = n2**2

Ez_data = []
for t in range(T):
    Hy[:-1] += (Ez[1:] - Ez[:-1]) * dt / (dx * 4e-7 * np.pi)
    Ez[1:] += (Hy[1:] - Hy[:-1]) * dt / (dx * 8.85e-12 * eps_r[1:])
    Ez[50] += np.exp(-0.5 * ((t - 100)/20)**2)
    if t % 10 == 0:
        Ez_data.append(Ez.copy())

Ez_data = np.array(Ez_data)

fig, ax = plt.subplots()
line, = ax.plot(Ez_data[0])
ax.set_ylim(-1.5, 1.5)
ax.set_title("FDTD DBR Propagation (Yee Grid)")
ax.set_xlabel("Position (nm)")
ax.set_ylabel("Ez")

def animate(i):
    line.set_ydata(Ez_data[i])
    return line,

ani = animation.FuncAnimation(fig, animate, frames=len(Ez_data), interval=50)
ani.save("yee_fdtd_dbr.gif", writer='pillow')
plt.close()
