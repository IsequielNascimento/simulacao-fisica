
---

# Simulações de Campo Magnético e Força de Lorentz

Este repositório contém **duas simulações interativas e didáticas** de eletromagnetismo baseadas no **capítulo 28 do livro *Fundamentos de Física 3 – Eletromagnetismo (Halliday, Resnick & Walker, 10ª edição*)**.

Ambas ilustram o comportamento de **partículas carregadas sob ação de um campo magnético**, evidenciando a **Força de Lorentz** e as propriedades vetoriais do movimento.

---

## 📦 Conteúdo

1. [`simulacao_campo_magnetico.py`](#-simulação-2d-interativa---campo-de-fios-e-partícula)

   * Campo magnético de **vários fios retilíneos infinitos**
   * Interação em tempo real com **botões e inputs**
   * Trajetória de **próton** ou **elétron** em um campo não uniforme

2. [`simulacao_movimento_helicoidal.py`](#-simulação-3d---movimento-helicoidal-em-campo-uniforme)

   * Movimento helicoidal em **campo uniforme**
   * Exibição 3D com **vetor velocidade** animado
   * Demonstração da decomposição de velocidade paralela e perpendicular

---

##  Requisitos

Instale as dependências com:

```bash
pip install matplotlib numpy scipy
```

---

##  Simulação 2D Interativa — Campo de Fios e Partícula

###  Conceito Físico

Cada fio retilíneo cria um campo magnético circular descrito por:

[
B = \frac{\mu_0 I}{2 \pi R}
]

O campo total é a soma vetorial dos campos de todos os fios.

A partícula sofre a **Força de Lorentz**:

[
\vec{F} = q(\vec{v} \times \vec{B}) \quad \Rightarrow \quad
F_x = q(-v_z B_y), ; F_y = q(v_z B_x)
]

O código integra numericamente a trajetória da partícula no plano (xy) para um (v_z) constante.

---

###  Como Rodar

```bash
python simulacao_campo_magnetico.py
```

Isso abrirá uma **janela interativa** do Matplotlib contendo:

* Setas do campo magnético (colormap “plasma”)
* Fios condutores (azul = corrente saindo do plano, vermelho = entrando)
* Botões à esquerda da tela para interagir

---

###  Controles Interativos

| Ação                 | Descrição                                        |
| -------------------- | ------------------------------------------------ |
| **Mover fio**        | Clique e arraste o fio no gráfico                |
| **Alterar corrente** | Digite no campo “Corrente (A)” e pressione Enter |
| **Adicionar fio**    | Cria um novo fio em posição aleatória            |
| **Remover fio**      | Remove o fio atualmente selecionado              |
| **Lançar Próton**    | Inicia uma partícula positiva (azul)             |
| **Lançar Elétron**   | Inicia uma partícula negativa (vermelha)         |

A partícula se move enquanto estiver dentro da área de simulação. Ao sair, é resetada automaticamente.

---

###  Estrutura do Código

| Função                  | Descrição                                       |
| ----------------------- | ----------------------------------------------- |
| `get_B_total_at()`      | Calcula o campo magnético total no ponto (x,y)  |
| `update_field()`        | Atualiza o quiver e os fios                     |
| `update_particula()`    | Aplica a Força de Lorentz e integra o movimento |
| `update_anim()`         | Atualiza a animação                             |
| `on_press`, `on_motion` | Eventos de arraste e clique nos fios            |
| `textbox_callback()`    | Atualiza a corrente inserida pelo usuário       |

---

##  Simulação 3D — Movimento Helicoidal em Campo Uniforme

Arquivo: `simulacao_movimento_helicoidal.py`


---

###  Parâmetros configuráveis

No início do código:

```python
q = 1.6e-19   # Carga (C)
m = 9.11e-31  # Massa (kg)
B = 1e-3      # Campo magnético (T)
v0 = 2e6      # Velocidade inicial (m/s)
angulo = 30   # Ângulo entre v e B (graus)
```

Esses parâmetros determinam o **raio** e o **passo da hélice**.

---

###  Como Rodar

```bash
python simulacao_movimento_helicoidal.py
```

O gráfico 3D exibirá:

* Uma **trajetória helicoidal azul**
* O **vetor velocidade (vermelho)** da partícula animado
* Um conjunto de **vetores do campo B** (azuis) apontando no eixo z

---

###  Estrutura do Código

| Seção             | Função                                            | Descrição                                 |
| ----------------- | ------------------------------------------------- | ----------------------------------------- |
| Cálculos iniciais | —                                                 | Define ω (frequência) e raio ciclotrônico |
| `update(frame)`   | Atualiza posição, linha, ponto e vetor velocidade |                                           |
| `FuncAnimation`   | Controla a animação quadro a quadro               |                                           |
| `ax.quiver()`     | Representa vetores do campo B                     |                                           |

---



---


---

## Referências

* **Halliday, Resnick & Walker – Fundamentos de Física 3: Eletromagnetismo (10ª Ed.)**
  Capítulo 28 – *O que produz um campo magnético?*
* Documentação oficial:

  * [Matplotlib](https://matplotlib.org/stable/)
  * [NumPy](https://numpy.org/)
  * [SciPy](https://scipy.org/)

---

> Feito por **Isequiel Nascimento, Leticia Sampaio de Souza, Marcos Martenier Santos Oliveira**
> Engenharia de Computação – Fortaleza/CE, 2025
> Disciplina: Físico-eletromagnetismo
> Projeto acadêmico: *Simulação de Campo Magnético e Movimento de Partículas*
