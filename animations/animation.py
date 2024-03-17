import matplotlib.pyplot as plt
from matplotlib.pyplot import style, figure, axes
from celluloid import Camera
import warnings
from Telegram_bot.solver.ERK2_l import ERK2_solver_length

warnings.filterwarnings('ignore')


def make_anime(x_0, y_0, v_x_0, v_y_0, end_time, name):
    r_0 = (x_0 ** 2 + y_0 ** 2) ** 0.5
    dl = r_0 / 2000
    ERK2_solution_length_step = ERK2_solver_length(x_0, y_0, v_x_0, v_y_0, dl, end_time)

    if ERK2_solution_length_step.any():
        del_step = int(len(ERK2_solution_length_step) / 100)
        ERK2_solution_length_step = ERK2_solution_length_step[::del_step]

        x_solution = ERK2_solution_length_step[:, 0]
        y_solution = ERK2_solution_length_step[:, 1]

        x_min = min(x_solution)
        x_max = max(x_solution)
        y_min = min(y_solution)
        y_max = max(y_solution)
        diameter = max(abs(x_max - x_min), abs(y_max - y_min))

        # Анимация отрисовки решения
        style.use('dark_background')

        fig = figure()
        camera = Camera(fig)
        ax = axes(xlim=(-1.2 * diameter, 1.2 * diameter), ylim=(-1.2 * diameter, 1.2 * diameter))
        ax.set_aspect('equal')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.grid()

        for m in range(len(ERK2_solution_length_step)):
            ax.plot(0, 0, 'yo', markersize=15)

            ax.plot(ERK2_solution_length_step[m, 0], ERK2_solution_length_step[m, 1], color='blue', marker='o',
                    markersize=7)
            ax.plot(ERK2_solution_length_step[:m + 1, 0], ERK2_solution_length_step[:m + 1, 1], color='blue', ls='--',
                    lw=2)

            camera.snap()
        animation = camera.animate(interval=200, repeat=False, blit=True)
        animation.save(rf'animations\{name}.gif', fps=30)
        return True
    else:
        return False
