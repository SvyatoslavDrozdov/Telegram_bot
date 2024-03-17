import numpy as np
import time

G = 6.674301515151515 * 10 ** (-11)
M_sun = 1.98847 * 10 ** 30


def new_f(u):
    real_func = np.zeros(4)
    real_func[0] = u[2]
    real_func[1] = u[3]
    real_func[2] = -G * M_sun * u[0] / (u[0] ** 2 + u[1] ** 2) ** 1.5
    real_func[3] = -G * M_sun * u[1] / (u[0] ** 2 + u[1] ** 2) ** 1.5

    sqr_root = 1
    for real_func_components in real_func:
        sqr_root += real_func_components ** 2
    sqr_root = sqr_root ** 0.5

    func = np.zeros(5)
    func[0] = real_func[0] / sqr_root
    func[1] = real_func[1] / sqr_root
    func[2] = real_func[2] / sqr_root
    func[3] = real_func[3] / sqr_root
    func[4] = 1 / sqr_root
    return func


def ERK2_solver_length(x_0, y_0, v_x_0, v_y_0, dl, end_time):
    start_calculation = time.time()

    u = np.zeros((1, 5))
    u_time_0 = 0
    u[0] = [x_0, y_0, v_x_0, v_y_0, u_time_0]

    point_number = 0
    while True:
        u = np.vstack((u, np.zeros((1, 5))))

        w_1 = new_f(u[point_number])
        w_2 = new_f(u[point_number] + dl * 2 / 3 * w_1)

        u[point_number + 1] = u[point_number] + dl * (1 / 4 * w_1 + 3 / 4 * w_2)

        if u[point_number + 1][4] >= end_time:
            break
        point_number += 1
        if point_number % 10 == 0:
            if time.time() - start_calculation >= 5:
                return np.array([0])
    return u
