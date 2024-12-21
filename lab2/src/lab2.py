import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Временной массив
t = np.linspace(0, 10, 1001)

# Зададим произвольные законы движения φ(t) и ψ(t)
phi = np.linspace(0, 2*np.pi, 1001)   # угол стержня OC от вертикали вниз
psi = np.linspace(0, 2*np.pi, 1001)   # угол CA от вертикали вверх

# Геометрические параметры
L = 1.0   # длина стержня OC
R = 0.5   # радиус диска
c = 10.0  # жесткость пружины (для анимации не важна)

# Координаты точки C
C_x = L * np.sin(phi)
C_y = -L * np.cos(phi)

# Координаты точки A
A_x = C_x + R * np.sin(psi)
A_y = C_y + R * np.cos(psi)

# Окружность диска
Alpha = np.linspace(0, 2*np.pi, 50)
xD = R*np.cos(Alpha) 
yD = R*np.sin(Alpha)

# Число витков спиральной пружины
N = 3
r1 = 0.05
r2 = 0.15
Beta0 = np.linspace(0,1,50*N+1)


fig = plt.figure(figsize=[8,8])
ax = fig.add_subplot(1,1,1)
ax.axis('equal')
system_length = (L + R)*1.2
ax.set(xlim=[-system_length,system_length], ylim=[-system_length,system_length])

# Неподвижная опора
ax.plot([-0.5,0.5],[0,0], color=[0,0,0], linewidth=3)

# Стержень
St = ax.plot([0, C_x[0]], [0, C_y[0]], color=[0.5,0.2,0.2], linewidth=4)[0]
# Диск
Disk = ax.plot(C_x[0]+xD, C_y[0]+yD, color=[0,0,1])[0]
# Точка C
Cpoint = ax.plot(C_x[0], C_y[0], 'o', color=[1,0,0], markersize=8)[0]
# Точка A
Apoint = ax.plot(A_x[0], A_y[0], 'o', color=[0,0.8,0], markersize=10, markerfacecolor=[0,1,0])[0]
# Линия CA
CA = ax.plot([C_x[0], A_x[0]], [C_y[0], A_y[0]], color=[0,0.7,0])[0]

# Спиральная пружина
# Углы для пружины
betas = Beta0*(2*np.pi*N + psi[0] + phi[0]) - phi[0]
r_spr = r1 + (r2 - r1)*Beta0
# Координаты пружины
xS = C_x[0] + r_spr * np.sin(betas)
yS = C_y[0] + r_spr * np.cos(betas)
SpiralSpring = ax.plot(xS, yS, color=[1,0.5,0.5])[0]


# Рассчёт для кадра i будет в функции kadr.
def kadr(i):
    cx = C_x[i]
    cy = C_y[i]
    ax_ = A_x[i]
    ay_ = A_y[i]

    # Обновление стержня, диска, точек
    St.set_data([0, cx],[0, cy])
    Disk.set_data([cx+xD], [cy+yD])
    Cpoint.set_data([cx], [cy])
    Apoint.set_data([ax_], [ay_])
    CA.set_data([cx, ax_],[cy, ay_])

    # Углы для пружины
    betas = Beta0*(2*np.pi*N + psi[i] + phi[i]) -phi[i]

    # Координаты пружины
    xS = cx + r_spr * np.sin(betas)
    yS = cy + r_spr * np.cos(betas)
    SpiralSpring.set_data(xS, yS)

    return [St, Disk, Cpoint, Apoint, CA, SpiralSpring]

kino = FuncAnimation(fig, kadr, interval=(t[1]-t[0])*100, frames=len(t))
plt.show()
