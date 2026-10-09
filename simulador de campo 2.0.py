import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation


class ElectricFieldSimulatorAnimated:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2)

        self.charges = []
        self.grid_size = 20
        self.k = 9e9

        self.ax.set_xlim(-self.grid_size, self.grid_size)
        self.ax.set_ylim(-self.grid_size, self.grid_size)
        self.ax.set_title('Campo Elétrico - Simulador(CODAI)')
        self.ax.set_xlabel('Posição X (m)')
        self.ax.set_ylabel('Posição Y (m)')
        self.ax.grid(True)

        self.add_buttons()

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        self.adding_positive = False
        self.adding_negative = False

        self.anim = None
        self.quiver = None
        self.X = self.Y = self.Ex = self.Ey = None
        self.phase = 0

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
        if self.anim:
            self.anim.event_source.stop()
        self.update_plot()
        print("Todas as cargas foram removidas.")

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        if self.adding_positive:
            self.charges.append((event.xdata, event.ydata, 1e-9))
            print(f"Carga positiva adicionada em ({event.xdata:.2f}, {event.ydata:.2f})")
            self.adding_positive = False
            self.update_plot()

        elif self.adding_negative:
            self.charges.append((event.xdata, event.ydata, -1e-9))
            print(f"Carga negativa adicionada em ({event.xdata:.2f}, {event.ydata:.2f})")
            self.adding_negative = False
            self.update_plot()

    def calculate_field(self, x, y):
        Ex, Ey = 0, 0
        for (xc, yc, q) in self.charges:
            dx, dy = x - xc, y - yc
            r = np.sqrt(dx**2 + dy**2)
            if r < 0.2:
                continue
            E = self.k * q / r**3
            Ex += E * dx
            Ey += E * dy
        return Ex, Ey

    def update_plot(self):
        self.ax.clear()
        self.ax.set_xlim(-self.grid_size, self.grid_size)
        self.ax.set_ylim(-self.grid_size, self.grid_size)
        self.ax.set_title('Campo Elétrico - Simulador Animado')
        self.ax.set_xlabel('Posição X (m)')
        self.ax.set_ylabel('Posição Y (m)')
        self.ax.grid(True)

        for (x, y, q) in self.charges:
            color = 'red' if q > 0 else 'blue'
            self.ax.scatter(x, y, c=color, s=500, edgecolors='black')
            self.ax.text(x, y, '+' if q > 0 else '-', ha='center', va='center', color='white')

        if not self.charges:
            self.fig.canvas.draw()
            return

        x = np.linspace(-self.grid_size, self.grid_size, 15)
        y = np.linspace(-self.grid_size, self.grid_size, 15)
        self.X, self.Y = np.meshgrid(x, y)
        self.Ex, self.Ey = np.zeros_like(self.X), np.zeros_like(self.Y)

        for i in range(self.X.shape[0]):
            for j in range(self.X.shape[1]):
                e_x, e_y = self.calculate_field(self.X[i, j], self.Y[i, j])
                self.Ex[i, j] = e_x
                self.Ey[i, j] = e_y

        E_norm = np.sqrt(self.Ex**2 + self.Ey**2)
        self.Ex = np.where(E_norm > 0, self.Ex / E_norm, 0)
        self.Ey = np.where(E_norm > 0, self.Ey / E_norm, 0)

        self.quiver = self.ax.quiver(self.X, self.Y, self.Ex, self.Ey,
                                     color='green', scale=30, width=0.003,
                                     headwidth=3, headlength=4)

        if self.anim:
            self.anim.event_source.stop()
        self.anim = FuncAnimation(self.fig, self.animate, frames=200, interval=100, blit=False, repeat=True)

        self.fig.canvas.draw()

    def animate(self, frame):
        phase_shift = np.sin(frame * 0.2) * 0.2
        self.quiver.set_UVC(self.Ex * (1 + phase_shift), self.Ey * (1 + phase_shift))
        return self.quiver,

    def show(self):
        plt.show()


simulator = ElectricFieldSimulatorAnimated()
simulator.show()
