import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches


class ElectricFieldSimulator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2)


        self.charges = []
        self.grid_size = 20
        self.k = 9e9


        self.ax.set_xlim(-self.grid_size, self.grid_size)
        self.ax.set_ylim(-self.grid_size, self.grid_size)
        self.ax.set_title('Campo Elétrico - Simulador Codai')
        self.ax.set_xlabel('Posição X (m)')
        self.ax.set_ylabel('Posição Y (m)')
        self.ax.grid(True)


        self.add_buttons()


        self.fig.canvas.mpl_connect('button_press_event', self.on_click)


        self.adding_positive = False
        self.adding_negative = False

    def add_buttons(self):

        ax_pos = plt.axes([0.2, 0.05, 0.15, 0.075])
        ax_neg = plt.axes([0.4, 0.05, 0.15, 0.075])
        ax_clear = plt.axes([0.6, 0.05, 0.15, 0.075])


        self.btn_pos = Button(ax_pos, 'Adicionar +')
        self.btn_neg = Button(ax_neg, 'Adicionar -')
        self.btn_clear = Button(ax_clear, 'Limpar')


        self.btn_pos.on_clicked(self.set_add_positive)
        self.btn_neg.on_clicked(self.set_add_negative)
        self.btn_clear.on_clicked(self.clear_all)

    def set_add_positive(self, event):
        self.adding_positive = True
        self.adding_negative = False
        print("Modo: Adicionar carga positiva (+1nC). Clique no gráfico para posicionar.")

    def set_add_negative(self, event):
        self.adding_positive = False
        self.adding_negative = True
        print("Modo: Adicionar carga negativa (-1nC). Clique no gráfico para posicionar.")

    def clear_all(self, event):
        self.charges = []
        self.update_plot()
        print("Todas as cargas foram removidas.")

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        if self.adding_positive:
            self.charges.append((event.xdata, event.ydata, 1e-9))  # +1nC
            print(f"Carga positiva adicionada em ({event.xdata:.2f}, {event.ydata:.2f})")
            self.adding_positive = False
            self.update_plot()

        elif self.adding_negative:
            self.charges.append((event.xdata, event.ydata, -1e-9))  # -1nC
            print(f"Carga negativa adicionada em ({event.xdata:.2f}, {event.ydata:.2f})")
            self.adding_negative = False
            self.update_plot()

    def calculate_field(self, x, y):
        Ex, Ey = 0, 0

        for charge in self.charges:
            xc, yc, q = charge
            dx = x - xc
            dy = y - yc
            r = np.sqrt(dx ** 2 + dy ** 2)

            if r < 0.1:
                continue

            E = self.k * q / r ** 3
            Ex += E * dx
            Ey += E * dy

        return Ex, Ey

    def update_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-self.grid_size, self.grid_size)
        self.ax.set_ylim(-self.grid_size, self.grid_size)
        self.ax.set_title('Simulador de Campo Elétrico')
        self.ax.set_xlabel('Posição X (m)')
        self.ax.set_ylabel('Posição Y (m)')
        self.ax.grid(True)


        for x, y, q in self.charges:
            color = 'red' if q > 0 else 'blue'
            self.ax.scatter(x, y, c=color, s=500 * abs(q) / 1e-9, edgecolors='black')
            sign = '+' if q > 0 else '-'
            self.ax.text(x, y, sign, ha='center', va='center', color='white')


        if self.charges:
            x = np.linspace(-self.grid_size, self.grid_size, 15)
            y = np.linspace(-self.grid_size, self.grid_size, 15)
            X, Y = np.meshgrid(x, y)

            Ex, Ey = np.zeros_like(X), np.zeros_like(Y)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    e_x, e_y = self.calculate_field(X[i, j], Y[i, j])
                    Ex[i, j] = e_x
                    Ey[i, j] = e_y


            E_norm = np.sqrt(Ex ** 2 + Ey ** 2)
            Ex_norm = np.where(E_norm > 0, Ex / E_norm, 0)
            Ey_norm = np.where(E_norm > 0, Ey / E_norm, 0)


            self.ax.quiver(X, Y, Ex_norm, Ey_norm,
                           color='green', scale=30, width=0.002,
                           headwidth=3, headlength=4)

        self.fig.canvas.draw()

    def show(self):
        plt.show()



simulator = ElectricFieldSimulator()
simulator.show()