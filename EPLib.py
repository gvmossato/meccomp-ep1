import numpy as np
import matplotlib.pyplot as plt

# ======= #
# Parte 1 #
# ======= #

def RK4(F: list, t0: float, Y0: list, h: float, tf: float) -> tuple:
    """
    Resolve um sistema de EDOs de primeira ordem pelo método
    de Runge Kutta de quarta ordem

    Args:
        F (list): funções a serem resolvidas
        t0 (float): valor inicial da variável independente
        Y0 (list): valores iniciais das variáveis dependentes
        h (foat): passo da variável independente
        tf (float): valor final da variável independente

    Returns:
        tuple: histórico de valores para Y e K1, respectivamente
    """
    Y_hist = []
    K1_hist = []

    Y = np.copy(Y0)
    T = np.arange(t0, tf+h, h)
    t = t0

    for t in T:
        K1 = np.array([f(t, Y) for f in F])
        K2 = np.array([f(t + 0.5*h, Y + 0.5*h*K1) for f in F])
        K3 = np.array([f(t + 0.5*h, Y + 0.5*h*K2) for f in F])
        K4 = np.array([f(t +     h, Y +     h*K3) for f in F])

        Y_hist.append(np.copy(Y))
        K1_hist.append(np.copy(K1))

        Y += (h/6) * (K1 + 2*K2 + 2*K3 + K4)

    return (T, np.transpose(Y_hist), np.transpose(K1_hist))


def get_scales(Y: np.ndarray) -> np.ndarray:
    """
    Para uma lista de vetores, ajusta a amplitude de cada um à
    mediana das amplitudes, através de um fator de escala 10^n
    (com n inteiro)

    Args:
        Y (np.ndarray): lista de vetores a terem suas amplitudes ajustadas

    Returns:
        np.ndarray: escalas que ajustam todos os vetores a um
                    intervalo próximo ao da amplitude mediana
    """
    n = len(Y)

    scales = np.zeros((n, 1))
    amplitudes = np.max(Y, axis=1) - np.min(Y, axis=1)
    median_idx = np.argsort(amplitudes)[n//2]

    for i in range(n):
        # a * 10**x == b => x == np.log10(b/a)
        power = np.log10(amplitudes[median_idx]/amplitudes[i])
        scales[i, 0] = np.round(power)

    return 10 ** scales


def scale_plot(
        x, Y,
        title='Gráfico',
        xlabel='Eixo x',
        ylabel='Eixo y',
        legend=[]
    ):
    """
    Plota múltiplas curvas ajustando um fator de escala a cada
    uma para assegurar a visualização adequada dos dados

    Args:
        x (np.ndarray): valores da variável do eixo x
        Y (np.ndarray): valores da(s) variável(is) do eixo y
        title (string): título do gráfico
        xlabel (string): legenda do eixo x
        ylabel (string): legenda do eixo y
        legend (list): legendas para cada curva (recebem a escala)
    """
    base10_scales = get_scales(Y)
    n = len(legend)

    scales_legend = [f"{legend[i]} × {base10_scales[i][0]:.0e}" for i in range(n)]

    plt.style.use('seaborn')
    plt.plot(x, (Y * base10_scales).T)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(scales_legend)
    plt.show()

    return

# ======= #
# Parte 2 #
# ======= #

def validate_step(h, contour_gcd):
    return contour_gcd / np.round(contour_gcd / h)

def gen_meshgrid(
    r_step: float, phi_step: float,
    r_start: float = 0.03, r_end: float = 0.08,
    phi_start: float = 0.0, phi_end: float = 40.0
    ) -> np.ndarray:

    h_r = validate_step(r_step, 0.01)
    h_phi = validate_step(phi_step, 2.0)

    r_axis = np.arange(r_start, r_end+h_r, h_r)
    phi_axis = np.deg2rad(np.arange(phi_start, phi_end+h_r, h_phi))

    r_vals, phi_vals = np.meshgrid(r_axis, phi_axis)

    x_vals = r_vals * np.cos(phi_vals)
    y_vals = r_vals * np.sin(phi_vals)

    return x_vals, y_vals

# ========== #
# Miscelania #
# ========== #

def validate_input(text: str, valid_inputs: list, default: str = '') -> str:
    """
    Adicona lógica de validação de entrada e valor de entrada padrão
    ao input do Python. Validações realizadas sempre com caracteres minúsculos.

    Args:
        text (str): texto a ser exibido ao solicitar input
        valid_inputs (list): lista de entradas aceitas
        default (str): entrada padrão caso o usuário não insira uma

    Returns:
        str: entrada do usuário devidamente validada
    """
    valid_inputs = [str(v) for v in valid_inputs]

    while True:
        user_input = input(text).lower() or default
        if user_input in valid_inputs: break
        print('Entrada inválida!')
    return user_input


def ctext(text: str, tag: str) -> str:
    """
    Aplica cor a uma string impressa no terminal, através de tags pré-definidas.
    As cores podem sofrer alterações conforme as configurações do terminal do usuário.

    Args:
        text (str): texto a ser colorido.
        tag (str): identificador que mapeia a cor desejada a um código
                   ASCII; tags válidas:
                   > 'r' -> Vermelho;
                   > 'g' -> Verde;
                   > 'y' -> Amarelo;
                   > 'b' -> Azul;
                   > 'm' -> Magenta;
                   > 'c' -> Ciano.

    Returns:
        str: string idêntica a text, exceto pelas tags de cor.
    """

    color_dict = {
        'r' : '\033[31m', # Red
        'g' : '\033[32m', # Green
        'y' : '\033[33m', # Yellow
        'b' : '\033[34m', # Blue
        'm' : '\033[35m', # Magenta
        'c' : '\033[36m'  # Cyan
    }

    # Aplica a tag de cor e reseta para a cor padrão do terminal do usuário.
    text = color_dict[tag] + text + '\033[0m'

    return text





# h: entrada do user -- tamanho passo
# n: número de passos

# h = mdc_contornos / k => k = mdc_contornos / h



# n =  max * k
# if n int: true
# else:

# k = 1/h