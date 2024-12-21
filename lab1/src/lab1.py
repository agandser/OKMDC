import matplotlib.pyplot as plt
import numpy as np
import sympy

from matplotlib.animation import FuncAnimation

def r(t):
    # Функция радиус-вектора материальной точки от времени
    return 1 + sympy.sin(5 * t)

def phi(t):
    # Функция угла материальной точки от времени
    return t

def Rot2D(X, Y, phi):
    # Поворот двумерной ДСК с помощью матрицы поворота
    X_r = X * np.cos(phi) - Y * np.sin(phi)
    Y_r = X * np.sin(phi) + Y * np.cos(phi)
    return X_r, Y_r

def main():
    t = sympy.Symbol("t")
    x = r(t) * sympy.cos(phi(t))
    y = r(t) * sympy.sin(phi(t))

    Vx = sympy.diff(x, t)
    Vy = sympy.diff(y, t)
    Wx = sympy.diff(Vx, t)
    Wy = sympy.diff(Vy, t)

    F_x = sympy.lambdify(t, x, "numpy")
    F_y = sympy.lambdify(t, y, "numpy")
    F_Vx = sympy.lambdify(t, Vx, "numpy")
    F_Vy = sympy.lambdify(t, Vy, "numpy")
    F_Wx = sympy.lambdify(t, Wx, "numpy")
    F_Wy = sympy.lambdify(t, Wy, "numpy")

    time_steps_amount = 1000
    T = np.linspace(0, 4 * np.pi, time_steps_amount)

    X = F_x(T)
    Y = F_y(T)
    VX = F_Vx(T)
    VY = F_Vy(T)
    WX = F_Wx(T)
    WY = F_Wy(T)

    V_phi = np.arctan2(VY, VX)
    W_phi = np.arctan2(WY, WX)

    # Добавим угол для радиус-вектора
    R_phi = np.arctan2(Y, X)

    # Масштабы стрелок
    V_scale = 4/10
    W_scale = 4/10
    # Масштаб для стрелки радиус-вектора
    R_scale = 4/10

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.axis("equal")
    ax1.set(
        xlim=[-8, 8],
        ylim=[-8, 8],
        title=(
            f"Радиус-вектор (R) – серый вектор (масштаб 1.0)\n"
            f"Скорость (V) – зелёный вектор (масштаб {V_scale})\n"
            f"Ускорение (W) – красный вектор (масштаб {W_scale})"
        ),
    )
    ax1.plot(X, Y)

    (point,) = ax1.plot(X[0], Y[0], marker="o")

    R_color = [0.5, 0.5, 0.5]  # серый
    (R_line,) = ax1.plot([0, X[0]], [0, Y[0]], color=R_color)

    # Вектор V (зелёный)
    V_color = [0, 0.7, 0]
    (V_line,) = ax1.plot(
        [X[0], X[0] + VX[0] * V_scale],
        [Y[0], Y[0] + VY[0] * V_scale],
        color=V_color,
    )

    # Вектор W (красный)
    W_color = [0.7, 0, 0]
    (W_line,) = ax1.plot(
        [X[0], X[0] + WX[0] * W_scale],
        [Y[0], Y[0] + WY[0] * W_scale],
        color=W_color,
    )

    # Стрелка для вектора V
    X_arr_V = np.array([-0.7, 0, -0.7]) * V_scale
    Y_arr_V = np.array([0.2, 0, -0.2]) * V_scale
    RX_V, RY_V = Rot2D(X_arr_V, Y_arr_V, V_phi[0])
    (V_arrow,) = ax1.plot(X[0] + VX[0] * V_scale + RX_V,
                          Y[0] + VY[0] * V_scale + RY_V,
                          color=V_color)

    # Стрелка для вектора W
    X_arr_W = np.array([-0.7, 0, -0.7]) * W_scale
    Y_arr_W = np.array([0.2, 0, -0.2]) * W_scale
    RX_W, RY_W = Rot2D(X_arr_W, Y_arr_W, W_phi[0])
    (W_arrow,) = ax1.plot(X[0] + WX[0] * W_scale + RX_W,
                          Y[0] + WY[0] * W_scale + RY_W,
                          color=W_color)

    # Стрелка для радиус-вектора R
    # По аналогии сделаем маленькую стрелку в конце радиус-вектора
    X_arr_R = np.array([-0.7, 0, -0.7]) * R_scale
    Y_arr_R = np.array([0.2, 0, -0.2]) * R_scale
    RX_R, RY_R = Rot2D(X_arr_R, Y_arr_R, R_phi[0])
    (R_arrow,) = ax1.plot(X[0] + RX_R, Y[0] + RY_R, color=R_color)

    def animate(i):
        # Точка
        point.set_data([X[i]], [Y[i]])

        # Радиус-вектор
        R_line.set_data([0, X[i]], [0, Y[i]])
        # Поворот и сдвиг стрелки радиус-вектора
        RX_R, RY_R = Rot2D(X_arr_R, Y_arr_R, R_phi[i])
        R_arrow.set_data(X[i] + RX_R, Y[i] + RY_R)

        # Вектор V
        V_line.set_data([X[i], X[i] + VX[i] * V_scale],
                        [Y[i], Y[i] + VY[i] * V_scale])
        RX_V, RY_V = Rot2D(X_arr_V, Y_arr_V, V_phi[i])
        V_arrow.set_data(X[i] + VX[i] * V_scale + RX_V,
                         Y[i] + VY[i] * V_scale + RY_V)

        # Вектор W
        W_line.set_data([X[i], X[i] + WX[i] * W_scale],
                        [Y[i], Y[i] + WY[i] * W_scale])
        RX_W, RY_W = Rot2D(X_arr_W, Y_arr_W, W_phi[i])
        W_arrow.set_data(X[i] + WX[i] * W_scale + RX_W,
                         Y[i] + WY[i] * W_scale + RY_W)

        return point, R_line, R_arrow, V_line, V_arrow, W_line, W_arrow

    animation = FuncAnimation(fig, animate, frames=time_steps_amount, interval=100)

    plt.show()

if __name__ == "__main__":
    main()
