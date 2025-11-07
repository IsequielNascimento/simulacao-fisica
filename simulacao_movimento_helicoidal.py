import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# ==========================
# Parâmetros físicos
# ==========================
q = 1.6e-19   # carga (C)
m = 9.11e-31  # massa (kg)
B = 1e-3      # campo magnético (T)
v0 = 2e6      # velocidade inicial (m/s)
angulo = 30   # ângulo entre v e B (graus)

# Componentes da velocidade inicial
v_par = v0 * np.cos(np.radians(angulo))   # paralela ao B
v_perp = v0 * np.sin(np.radians(angulo))  # perpendicular a B

# Frequência ciclotrônica e raio
omega = q * B / m
raio = m * v_perp / (q * B)

# Vetor de tempo
t = np.linspace(0, 2e-7, 1000)

# Trajetória helicoidal
x = raio * np.cos(omega * t)
y = raio * np.sin(omega * t)
z = v_par * t

# ==========================
# Criação da figura 3D
# ==========================
fig = plt.figure(figsize=(9,7))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-raio*1.5, raio*1.5)
ax.set_ylim(-raio*1.5, raio*1.5)
ax.set_zlim(0, max(z))
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_zlabel("z (m)")
ax.set_title("Movimento helicoidal de uma partícula carregada em um campo magnético")

# ==========================
# Campo magnético (setas azuis)
# ==========================
# Criar uma grade de vetores B apontando no eixo z
bx, by = np.meshgrid(np.linspace(-raio, raio, 4), np.linspace(-raio, raio, 4))
bz = np.ones_like(bx) * 0.5  # direção z
ax.quiver(bx, by, 0, 0, 0, bz, color='b', length=raio*0.5, normalize=True, alpha=0.5)

# ==========================
# Elementos gráficos animados
# ==========================
linha, = ax.plot([], [], [], 'dodgerblue', lw=2, label="Trajetória")
ponto, = ax.plot([], [], [], 'ro', markersize=6, label="Partícula")
velocidade = None

# ==========================
# Função de atualização da animação
# ==========================
def update(frame):
    global velocidade
    linha.set_data(x[:frame], y[:frame])
    linha.set_3d_properties(z[:frame])
    ponto.set_data([x[frame]], [y[frame]])
    ponto.set_3d_properties([z[frame]])

    # Remove vetor de velocidade antigo, se existir
    if velocidade:
        velocidade.remove()

    # Calcula vetor de velocidade instantânea
    vx = -raio * omega * np.sin(omega * t[frame])
    vy =  raio * omega * np.cos(omega * t[frame])
    vz = v_par

    escala = 2e-8
    velocidade = ax.quiver(
        x[frame], y[frame], z[frame],
        vx, vy, vz,
        color='r', length=escala, normalize=True
    )

    return linha, ponto, velocidade

# ==========================
# Criar animação
# ==========================
ani = FuncAnimation(fig, update, frames=len(t), interval=10, blit=False)

# ==========================
# Configurações finais
# ==========================
ax.legend()
ax.grid(True)
plt.tight_layout()
plt.show()
