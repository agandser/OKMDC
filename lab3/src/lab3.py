import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

# Заданные параметры системы
m1 = 2   # кг
m2 = 3.0   # кг
m3 = 1   # кг
l  = 1.0   # м
r  = 0.5   # м
c  = 10  # Н·м
g  = 9.81  # м/с^2

# Начальные условия
phi0     = 0      # рад
psi0     = 0      # рад
dphi0    = 0     # рад/с
dpsi0    = 0    # рад/с
y0 = [phi0, psi0, dphi0, dpsi0]

# Временной интервал интегрирования
t_fin = 20.0
Nt    = 1001
t     = np.linspace(0, t_fin, Nt)


# Функция для вычисления правых частей уравнений движения
def EqOfMovement(y, t, m1, m2, m3, l, r, c, g):
    # Переменные состояния:
    # y = [phi, psi, dphi, dpsi]
    phi  = y[0]
    psi  = y[1]
    dphi = y[2]
    dpsi = y[3]

    # Частные выражения
    phi_psi = phi + psi
    sin_pp = np.sin(phi_psi)
    cos_pp = np.cos(phi_psi)

    # Матрица системы (левой части)
    A11 = (m1/3.0 + m2 + m3)*l
    A12 = m3*r*cos_pp
    A21 = m3*l*cos_pp
    A22 = (m2/2.0 + m3)*r

    # Из уравнений:

    B1 = -((m1/2.0) + m2 + m3)*g*np.sin(phi) - (c/l)*(phi+psi) + m3*r*(dpsi**2)*sin_pp


    B2 = -m3*g*np.sin(psi) - (c/r)*(phi+psi) + m3*l*(dphi**2)*sin_pp

    # Решаем систему уравнений для ddphi и ddpsi
    det = A11*A22 - A21*A12
    ddphi = (B1*A22 - B2*A12)/det
    ddpsi = (A11*B2 - A21*B1)/det

    # Формируем вектор производных
    # y' = [dphi, dpsi, ddphi, ddpsi]
    dy = np.zeros_like(y)
    dy[0] = dphi
    dy[1] = dpsi
    dy[2] = ddphi
    dy[3] = ddpsi

    return dy

# Численное интегрирование
Y = odeint(EqOfMovement, y0, t, (m1,m2,m3,l,r,c,g))

phi  = Y[:,0]
psi  = Y[:,1]
dphi = Y[:,2]
dpsi = Y[:,3]

# Найдем ускорения для вычисления реакций R_x, R_y
# Для этого снова применим EqOfMovement или вычислим ddphi, ddpsi непосредственно
dd = np.array([EqOfMovement(Y[i,:], t[i], m1,m2,m3,l,r,c,g) for i in range(len(t))])
ddphi = dd[:,2]
ddpsi = dd[:,3]

# Вычисление реакций в шарнире O по заданным формулам
M = (m1/2.0)+m2+m3

R_x = -M*l*(ddphi*np.sin(phi) + dphi**2*np.cos(phi)) + m3*r*(ddpsi*np.sin(psi)+dpsi**2*np.cos(psi)) - (m1+m2+m3)*g
R_y = M*l*(ddphi*np.cos(phi) - dphi**2*np.sin(phi)) + m3*r*(ddpsi*np.cos(psi)-dpsi**2*np.sin(psi))

# Построение графиков φ(t), ψ(t), R_x(t), R_y(t)
fig0 = plt.figure(figsize=[10,8])
ax1 = fig0.add_subplot(2,2,1)
ax1.plot(t, phi, 'r')
ax1.set_title('$\\varphi(t)$')
ax1.grid(True)

ax2 = fig0.add_subplot(2,2,2)
ax2.plot(t, psi, 'g')
ax2.set_title('$\\psi(t)$')
ax2.grid(True)

ax3 = fig0.add_subplot(2,2,3)
ax3.plot(t, R_x, 'b')
ax3.set_title('$R_x(t)$')
ax3.grid(True)

ax4 = fig0.add_subplot(2,2,4)
ax4.plot(t, R_y, 'k')
ax4.set_title('$R_y(t)$')
ax4.grid(True)


# Координаты точки C
C_x = l*np.sin(phi)
C_y = -l*np.cos(phi)

# Координаты точки A
A_x = C_x + r*np.sin(psi)
A_y = C_y + r*np.cos(psi)

# Окружность диска
Alpha = np.linspace(0, 2*np.pi, 50)
xD = r*np.cos(Alpha) 
yD = r*np.sin(Alpha)

# Число витков спиральной пружины
N = 3
r1 = 0.05
r2 = 0.15
Beta0 = np.linspace(0,1,50*N+1)
r_spr = r1 + (r2 - r1)*Beta0

fig = plt.figure(figsize=[8,8])
ax = fig.add_subplot(1,1,1)
ax.axis('equal')
system_length = (l + r)*1.2
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

# Спиральная пружина (при phi=psi=0 не деформирована)
betas = Beta0*(2*np.pi*N + psi[0] + phi[0]) - phi[0]
xS = C_x[0] + r_spr*np.sin(betas)
yS = C_y[0] + r_spr*np.cos(betas)
SpiralSpring = ax.plot(xS, yS, color=[1,0.5,0.5])[0]

def kadr(i):
    cx = C_x[i]
    cy = C_y[i]
    ax_ = A_x[i]
    ay_ = A_y[i]

    St.set_data([0, cx],[0, cy])
    Disk.set_data([cx+xD], [cy+yD])
    Cpoint.set_data([cx], [cy])
    Apoint.set_data([ax_], [ay_])
    CA.set_data([cx, ax_],[cy, ay_])

    # Углы для пружины
    betas = Beta0*(2*np.pi*N + psi[i] + phi[i]) -phi[i]
    xS = cx + r_spr * np.sin(betas)
    yS = cy + r_spr * np.cos(betas)
    SpiralSpring.set_data(xS, yS)

    return [St, Disk, Cpoint, Apoint, CA, SpiralSpring]

kino = FuncAnimation(fig, kadr, interval=(t[1]-t[0])*100, frames=len(t), blit=False)
plt.show()