import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox

x = np.linspace(0, 10, 1000)
t = np.linspace(0, 20, 1000)

amplitude_onda1, frequencia_onda1, velocidade_onda1 = 1.0, 0.5, 1.0
amplitude_onda2, frequencia_onda2, velocidade_onda2 = 0.8, 0.3, 1.5

direcao_onda1, direcao_onda2 = 1, 1
fase_graus_onda1, fase_graus_onda2 = 0, 0

paused = False
frame_idx = 0
mostrar_onda1 = True
mostrar_onda2 = True
mostrar_superposicao = True

_cache = {}

def numero_de_onda(frequencia, velocidade):
    return 2 * np.pi * frequencia / velocidade

def precalcular_ondas(A1, A2, f1, f2, v1, v2, direcao1, direcao2, fase1_graus, fase2_graus):
    cache_key = (A1, A2, f1, f2, v1, v2, direcao1, direcao2, fase1_graus, fase2_graus)
    if cache_key not in _cache:
        omega1, omega2 = 2*np.pi*f1, 2*np.pi*f2
        k1, k2 = numero_de_onda(f1, v1), numero_de_onda(f2, v2)
        fase1_rad = np.radians(fase1_graus)
        fase2_rad = np.radians(fase2_graus)
        y1_all = np.zeros((len(t), len(x)))
        y2_all = np.zeros((len(t), len(x)))
        for i, time_val in enumerate(t):
            y1_all[i] = A1 * np.sin(direcao1 * k1 * x - omega1 * time_val + fase1_rad)
            y2_all[i] = A2 * np.sin(direcao2 * k2 * x - omega2 * time_val + fase2_rad)
        _cache[cache_key] = (y1_all, y2_all, omega1, omega2, k1, k2)
    return _cache[cache_key]

fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(left=0.1, bottom=0.50)

linha_onda1, = ax.plot([], [], 'b-', lw=2, label='Onda 1', alpha=0.7)
linha_onda2, = ax.plot([], [], 'r-', lw=2, label='Onda 2', alpha=0.7)
linha_superposicao, = ax.plot([], [], 'g-', lw=3, label='Superposição')

texto_info = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9),
                     verticalalignment='top')

ax.set_xlim(0, 10)
ax.set_ylim(-3, 3)
ax.set_xlabel('Posição (x)')
ax.set_ylabel('Amplitude (y)')
ax.set_title('Simulação de Superposição de Ondas - Codai')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

ax_amp1 = plt.axes([0.15, 0.40, 0.5, 0.02])
ax_freq1 = plt.axes([0.15, 0.37, 0.5, 0.02])
ax_vel1 = plt.axes([0.15, 0.34, 0.5, 0.02])

ax_amp2 = plt.axes([0.15, 0.30, 0.5, 0.02])
ax_freq2 = plt.axes([0.15, 0.27, 0.5, 0.02])
ax_vel2 = plt.axes([0.15, 0.24, 0.5, 0.02])

slider_amplitude_onda1 = Slider(ax_amp1, 'Amp Onda 1', 0.1, 3.0, valinit=amplitude_onda1)
slider_frequencia_onda1 = Slider(ax_freq1, 'Freq Onda 1', 0.1, 2.0, valinit=frequencia_onda1)
slider_velocidade_onda1 = Slider(ax_vel1, 'Vel Onda 1', 0.1, 3.0, valinit=velocidade_onda1)

slider_amplitude_onda2 = Slider(ax_amp2, 'Amp Onda 2', 0.1, 3.0, valinit=amplitude_onda2)
slider_frequencia_onda2 = Slider(ax_freq2, 'Freq Onda 2', 0.1, 2.0, valinit=frequencia_onda2)
slider_velocidade_onda2 = Slider(ax_vel2, 'Vel Onda 2', 0.1, 3.0, valinit=velocidade_onda2)

for s in [slider_amplitude_onda1, slider_frequencia_onda1, slider_velocidade_onda1,
          slider_amplitude_onda2, slider_frequencia_onda2, slider_velocidade_onda2]:
    try:
        s.valtext.set_visible(False)
    except Exception:
        pass  

# -------------------- TextBoxes (substituem os números) --------------------
ax_text_amp1 = plt.axes([0.64, 0.40, 0.04, 0.03])
ax_text_freq1 = plt.axes([0.64, 0.37, 0.04, 0.03])
ax_text_vel1 = plt.axes([0.64, 0.34, 0.04, 0.03])

ax_text_amp2 = plt.axes([0.64, 0.30, 0.04, 0.03])
ax_text_freq2 = plt.axes([0.64, 0.27, 0.04, 0.03])
ax_text_vel2 = plt.axes([0.64, 0.24, 0.04, 0.03])

tb_amp1 = TextBox(ax_text_amp1, '', initial=f"{amplitude_onda1:.2f}")
tb_freq1 = TextBox(ax_text_freq1, '', initial=f"{frequencia_onda1:.2f}")
tb_vel1 = TextBox(ax_text_vel1, '', initial=f"{velocidade_onda1:.2f}")

tb_amp2 = TextBox(ax_text_amp2, '', initial=f"{amplitude_onda2:.2f}")
tb_freq2 = TextBox(ax_text_freq2, '', initial=f"{frequencia_onda2:.2f}")
tb_vel2 = TextBox(ax_text_vel2, '', initial=f"{velocidade_onda2:.2f}")

ax_fase1 = plt.axes([0.15, 0.19, 0.2, 0.03])
ax_fase2 = plt.axes([0.15, 0.15, 0.2, 0.03])
ax_btn_fase1 = plt.axes([0.36, 0.19, 0.08, 0.03])
ax_btn_fase2 = plt.axes([0.36, 0.15, 0.08, 0.03])

input_fase_onda1 = TextBox(ax_fase1, 'Fase Onda 1 (°): ', initial='0')
input_fase_onda2 = TextBox(ax_fase2, 'Fase Onda 2 (°): ', initial='0')
btn_aplicar_fase1 = Button(ax_btn_fase1, 'Aplicar')
btn_aplicar_fase2 = Button(ax_btn_fase2, 'Aplicar')

ax_start = plt.axes([0.70, 0.40, 0.08, 0.04])
ax_pause = plt.axes([0.79, 0.40, 0.08, 0.04])
ax_reset = plt.axes([0.88, 0.40, 0.08, 0.04])
ax_toggle1 = plt.axes([0.70, 0.34, 0.08, 0.04])
ax_toggle2 = plt.axes([0.79, 0.34, 0.08, 0.04])
ax_toggle_sum = plt.axes([0.88, 0.34, 0.08, 0.04])
ax_inverter1 = plt.axes([0.70, 0.28, 0.08, 0.04])
ax_inverter2 = plt.axes([0.79, 0.28, 0.08, 0.04])

btn_start = Button(ax_start, 'Iniciar')
btn_pause = Button(ax_pause, 'Pausar')
btn_reset = Button(ax_reset, 'Resetar')
btn_toggle1 = Button(ax_toggle1, 'Onda 1')
btn_toggle2 = Button(ax_toggle2, 'Onda 2')
btn_toggle_sum = Button(ax_toggle_sum, 'Soma')
btn_inverter1 = Button(ax_inverter1, 'Inverter 1')
btn_inverter2 = Button(ax_inverter2, 'Inverter 2')

def init():
    linha_onda1.set_data([], [])
    linha_onda2.set_data([], [])
    linha_superposicao.set_data([], [])
    texto_info.set_text('')
    return linha_onda1, linha_onda2, linha_superposicao, texto_info

def update_wave_values(val=None):
    """Chamado quando sliders mudam; limpa cache e força atualização (animate pegará)"""
    global _cache
    _cache.clear()

def aplicar_fase1(event):
    global fase_graus_onda1, _cache
    try:
        fase_graus_onda1 = float(input_fase_onda1.text)
        _cache.clear()
    except ValueError:
        print("Valor inválido para fase.")

def aplicar_fase2(event):
    global fase_graus_onda2, _cache
    try:
        fase_graus_onda2 = float(input_fase_onda2.text)
        _cache.clear()
    except ValueError:
        print("Valor inválido para fase.")

def update_animation():
    global frame_idx
    if paused:
        return linha_onda1, linha_onda2, linha_superposicao, texto_info

    frame_idx = (frame_idx + 1) % len(t)

    A1 = slider_amplitude_onda1.val
    A2 = slider_amplitude_onda2.val
    f1 = slider_frequencia_onda1.val
    f2 = slider_frequencia_onda2.val
    v1 = slider_velocidade_onda1.val
    v2 = slider_velocidade_onda2.val

    y1_all, y2_all, omega1, omega2, k1, k2 = precalcular_ondas(
        A1, A2, f1, f2, v1, v2, direcao_onda1, direcao_onda2, fase_graus_onda1, fase_graus_onda2
    )

    y1 = y1_all[frame_idx]
    y2 = y2_all[frame_idx]
    y_sum = y1 + y2

    linha_onda1.set_data(x, y1 if mostrar_onda1 else np.full_like(x, np.nan))
    linha_onda2.set_data(x, y2 if mostrar_onda2 else np.full_like(x, np.nan))
    linha_superposicao.set_data(x, y_sum if mostrar_superposicao else np.full_like(x, np.nan))

    T1 = 1/f1 if f1 != 0 else np.inf
    T2 = 1/f2 if f2 != 0 else np.inf
    lambda1 = 2*np.pi/k1 if k1 != 0 else np.inf
    lambda2 = 2*np.pi/k2 if k2 != 0 else np.inf

    texto_info.set_text(
        f"Onda 1: ω={omega1:.2f}, T={T1:.2f}, λ={lambda1:.2f}, Dir={'→' if direcao_onda1 > 0 else '←'}, φ={fase_graus_onda1}°\n"
        f"Onda 2: ω={omega2:.2f}, T={T2:.2f}, λ={lambda2:.2f}, Dir={'→' if direcao_onda2 > 0 else '←'}, φ={fase_graus_onda2}°"
    )

    return linha_onda1, linha_onda2, linha_superposicao, texto_info

def animate(i):
    return update_animation()

def start(event):
    global paused
    paused = False

def pause(event):
    global paused
    paused = True

def reset(event):
    global frame_idx, _cache, fase_graus_onda1, fase_graus_onda2
    frame_idx = 0
    _cache.clear()
    fase_graus_onda1 = fase_graus_onda2 = 0
    input_fase_onda1.set_val('0')
    input_fase_onda2.set_val('0')
    slider_amplitude_onda1.reset()
    slider_frequencia_onda1.reset()
    slider_velocidade_onda1.reset()
    slider_amplitude_onda2.reset()
    slider_frequencia_onda2.reset()
    slider_velocidade_onda2.reset()

def toggle1(event):
    global mostrar_onda1
    mostrar_onda1 = not mostrar_onda1
    btn_toggle1.label.set_text('Onda 1: ' + ('ON' if mostrar_onda1 else 'OFF'))

def toggle2(event):
    global mostrar_onda2
    mostrar_onda2 = not mostrar_onda2
    btn_toggle2.label.set_text('Onda 2: ' + ('ON' if mostrar_onda2 else 'OFF'))

def toggle_sum(event):
    global mostrar_superposicao
    mostrar_superposicao = not mostrar_superposicao
    btn_toggle_sum.label.set_text('Soma: ' + ('ON' if mostrar_superposicao else 'OFF'))

def inverter1(event):
    global direcao_onda1, _cache
    direcao_onda1 *= -1
    _cache.clear()

def inverter2(event):
    global direcao_onda2, _cache
    direcao_onda2 *= -1
    _cache.clear()
def bind_slider_textbox(slider, textbox, fmt="{:.2f}"):
 
    def on_slider(val):
        textbox.set_val(fmt.format(slider.val))
       
        update_wave_values(val)
    slider.on_changed(on_slider)

    
    def on_text_submit(text):
        try:
            val = float(text)
            
            if val < slider.valmin:
                val = slider.valmin
            if val > slider.valmax:
                val = slider.valmax
            slider.set_val(val) 
        except ValueError:
            
            textbox.set_val(fmt.format(slider.val))
    textbox.on_submit(on_text_submit)


bind_slider_textbox(slider_amplitude_onda1, tb_amp1)
bind_slider_textbox(slider_frequencia_onda1, tb_freq1)
bind_slider_textbox(slider_velocidade_onda1, tb_vel1)
bind_slider_textbox(slider_amplitude_onda2, tb_amp2)
bind_slider_textbox(slider_frequencia_onda2, tb_freq2)
bind_slider_textbox(slider_velocidade_onda2, tb_vel2)

btn_aplicar_fase1.on_clicked(aplicar_fase1)
btn_aplicar_fase2.on_clicked(aplicar_fase2)

btn_start.on_clicked(start)
btn_pause.on_clicked(pause)
btn_reset.on_clicked(reset)
btn_toggle1.on_clicked(toggle1)
btn_toggle2.on_clicked(toggle2)
btn_toggle_sum.on_clicked(toggle_sum)
btn_inverter1.on_clicked(inverter1)
btn_inverter2.on_clicked(inverter2)


for s, tb in [
    (slider_amplitude_onda1, tb_amp1), (slider_frequencia_onda1, tb_freq1), (slider_velocidade_onda1, tb_vel1),
    (slider_amplitude_onda2, tb_amp2), (slider_frequencia_onda2, tb_freq2), (slider_velocidade_onda2, tb_vel2)
]:
    tb.set_val(f"{s.val:.2f}")


toggle1(None)
toggle2(None)
toggle_sum(None)

ani = FuncAnimation(fig, animate, init_func=init, frames=len(t), interval=20, blit=True)
plt.show()
