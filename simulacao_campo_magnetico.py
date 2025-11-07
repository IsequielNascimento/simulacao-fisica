import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
from matplotlib.animation import FuncAnimation
import scipy.constants as const
import random
from collections import deque

def get_B_total_at(x_ponto, y_ponto, fios):
    mu_0 = const.mu_0
    Bx_total, By_total = 0.0, 0.0
    for fio in fios:
        rx = x_ponto - fio['x']
        ry = y_ponto - fio['y']
        R2 = rx**2 + ry**2
        if R2 == 0:
            continue
        R = np.sqrt(R2)
        B = (mu_0 * fio['corrente']) / (2 * np.pi * R)
        Bx_total += B * (-ry / R)
        By_total += B * (rx / R)
    return Bx_total, By_total

lista_de_fios = [{'x': 0.0, 'y': 0.0, 'corrente': 10.0}]
fio_sel = 0

particula = {
    'm': const.proton_mass,
    'q': const.e,
    'vz': 50000.0,
    'pos_xy': np.array([-10.0, 0.0]),
    'vel_xy': np.array([0.0, 15000.0]),
    'ativo': False,
    'tipo': 'proton'
}

trail = deque(maxlen=1000)

DT = 1e-7
PASSOS = 50

x_grid = np.linspace(-20, 20, 20)
y_grid = np.linspace(-20, 20, 20)
X, Y = np.meshgrid(x_grid, y_grid)

fig = plt.figure(figsize=(14, 10))
fig.subplots_adjust(left=0.35, right=0.98, bottom=0.05, top=0.95)
ax = fig.add_subplot(111)
ax.set_title("Simulação Interativa de Campo B com Partícula de Teste")
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect("equal", adjustable="box")
ax.grid(True)

quiver_plot = None
fio_plots = []
particle_plot = None
particle_trail = None
textbox_corrente = None

def update_field():
    global quiver_plot, fio_plots
    Bx, By = np.zeros_like(X), np.zeros_like(Y)
    for i in range(len(x_grid)):
        for j in range(len(y_grid)):
            Bx[i, j], By[i, j] = get_B_total_at(X[i, j], Y[i, j], lista_de_fios)
    if quiver_plot:
        quiver_plot.remove()
    for p in fio_plots:
        p.remove()
    fio_plots.clear()
    mag = np.sqrt(Bx**2 + By**2)
    quiver_plot = ax.quiver(X, Y, Bx, By, mag, cmap='plasma', scale=None)
    for i, fio in enumerate(lista_de_fios):
        edge = 'lime' if i == fio_sel else 'black'
        c = 'blue' if fio['corrente'] > 0 else 'red'
        p, = ax.plot(fio['x'], fio['y'], 'o', ms=15, mfc=c, mec=edge, mew=3)
        fio_plots.append(p)
    fig.canvas.draw_idle()

def update_particula(dt):
    if not particula['ativo']:
        return
    pos = particula['pos_xy']
    vel = particula['vel_xy']
    Bx, By = get_B_total_at(pos[0], pos[1], lista_de_fios)
    q = particula['q']
    m = particula['m']
    vz = particula['vz']
    Fx = q * (-vz * By)
    Fy = q * ( vz * Bx)
    ax_ = Fx / m
    ay_ = Fy / m
    vel = vel + np.array([ax_ * dt, ay_ * dt])
    pos = pos + vel * dt
    if abs(pos[0]) > 50 or abs(pos[1]) > 50:
        particula['ativo'] = False
        trail.clear()
        return
    particula['vel_xy'] = vel
    particula['pos_xy'] = pos
    trail.append((pos[0], pos[1]))

def init_anim():
    global particle_plot, particle_trail
    particle_plot, = ax.plot([], [], 'o', color='green', markersize=8, zorder=8)
    particle_trail, = ax.plot([], [], '-', color='green', alpha=0.5, zorder=7)
    return particle_plot, particle_trail

def update_anim(frame):
    for _ in range(PASSOS):
        update_particula(DT)

    if particula['ativo']:
        cor = 'blue' if particula['tipo'] == 'proton' else 'red'
        x = particula['pos_xy'][0]
        y = particula['pos_xy'][1]

        particle_plot.set_data([x], [y])
        particle_plot.set_color(cor)
        particle_trail.set_color(cor)

        if trail:
            x_trail, y_trail = zip(*trail)
            particle_trail.set_data(x_trail, y_trail)
        else:
            particle_trail.set_data([], [])
    else:
        particle_plot.set_data([], [])
        particle_trail.set_data([], [])

    return particle_plot, particle_trail

dragging = False
offset_x, offset_y = 0, 0
def on_press(event):
    global dragging, fio_sel, offset_x, offset_y, textbox_corrente
    if event.inaxes != ax:
        return
    for i in range(len(lista_de_fios) - 1, -1, -1):
        fio = lista_de_fios[i]
        dist_sq = (event.xdata - fio['x'])**2 + (event.ydata - fio['y'])**2
        if dist_sq < 0.2**2:
            dragging = True
            fio_sel = i
            offset_x = event.xdata - fio['x']
            offset_y = event.ydata - fio['y']
            if textbox_corrente:
                textbox_corrente.set_val(str(fio['corrente']))
            update_field()
            return

def on_release(event):
    global dragging
    dragging = False

def on_motion(event):
    if dragging and event.inaxes == ax and fio_sel is not None:
        fio = lista_de_fios[fio_sel]
        fio['x'] = event.xdata - offset_x
        fio['y'] = event.ydata - offset_y
        update_field()

def textbox_callback(text):
    global fio_sel
    try:
        val = float(text)
    except ValueError:
        textbox_corrente.set_val(str(lista_de_fios[fio_sel]['corrente']))
        return
    lista_de_fios[fio_sel]['corrente'] = val
    update_field()

def add_fio(event):
    global fio_sel
    novo = {
        'x': random.uniform(-10, 10),
        'y': random.uniform(-10, 10),
        'corrente': random.choice([10, -10])
    }
    lista_de_fios.append(novo)
    fio_sel = len(lista_de_fios) - 1
    textbox_corrente.set_val(str(novo['corrente']))
    update_field()

def rem_fio(event):
    global fio_sel
    if not lista_de_fios:
        return
    lista_de_fios.pop(fio_sel)
    if len(lista_de_fios) == 0:
        fio_sel = None
        textbox_corrente.set_val("0")
    else:
        fio_sel = len(lista_de_fios) - 1
        textbox_corrente.set_val(str(lista_de_fios[fio_sel]['corrente']))
    update_field()

def lancar(tipo):
    trail.clear()
    particula['ativo'] = True
    particula['pos_xy'] = np.array([-10.0, random.uniform(-3, 3)])
    particula['vel_xy'] = np.array([20000.0, 0.0])
    if tipo == 'proton':
        particula['tipo'] = 'proton'
        particula['m'] = const.proton_mass
        particula['q'] = const.e
    else:
        particula['tipo'] = 'electron'
        particula['m'] = const.electron_mass
        particula['q'] = -const.e

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

# widgets
ax_box = plt.axes([0.05, 0.85, 0.25, 0.05])
textbox_corrente = TextBox(ax_box, 'Corrente (A): ', initial=str(lista_de_fios[0]['corrente']))
textbox_corrente.on_submit(textbox_callback)

ax_add = plt.axes([0.05, 0.75, 0.25, 0.05])
ax_rem = plt.axes([0.05, 0.68, 0.25, 0.05])
ax_prot = plt.axes([0.05, 0.58, 0.25, 0.05])
ax_ele = plt.axes([0.05, 0.51, 0.25, 0.05])

btn_add = Button(ax_add, 'Adicionar Fio')
btn_rem = Button(ax_rem, 'Remover Fio')
btn_prot = Button(ax_prot, 'Lançar Próton')
btn_ele = Button(ax_ele, 'Lançar Elétron')

btn_add.on_clicked(add_fio)
btn_rem.on_clicked(rem_fio)
btn_prot.on_clicked(lambda e: lancar('proton'))
btn_ele.on_clicked(lambda e: lancar('electron'))

ani = FuncAnimation(fig, update_anim, init_func=init_anim, interval=20, blit=False)
update_field()

if __name__ == "__main__":
    try:
        plt.show()
    except KeyboardInterrupt:
        pass
