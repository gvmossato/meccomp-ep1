from turtle import width
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go

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
    scales_legend = [
        f"{legend[i]} × {base10_scales[i][0]:.0e}" for i in range(len(legend))
    ]

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

class Plate:
    def __init__(self, r_range, phi_range, params, materials):
        self.boundaries = params['regions']
        self.coeffs_formula = params['coeffs']
        self.colors = params['colors']
        self.initial = params['initial']
        self.materials = materials

        self.h_r, self.h_phi, self.r_vals, self.phi_vals = self._gen_range(r_range, phi_range)
        self.base_matrix = self._gen_base_matrix(len(self.phi_vals), len(self.r_vals))
        self.x_grid, self.y_grid, self.meshgrid = self._gen_grids()

    def _validate_step(self, h: float, contour_gcd: float):
        """
        Realiza a validação do passo para o meshgrid, assegurando que os
        contornos sejam devidamente representados

        Args:
            h (float): passo a ser validado
            contour_gcd (float): máximo divisor comum dos extremos dos contornos
                                para o eixo
        """
        return contour_gcd / np.round(contour_gcd / h)

    def _get_point_params(self, r, phi):
        for i in range(len(self.boundaries)):
            lower_r, upper_r, lower_phi, upper_phi = self.boundaries[i]

            r_tests = [
                lower_r <= r <= upper_r,
                np.isclose(r, lower_r) or np.isclose(r, upper_r),
            ]
            phi_tests = [
                lower_phi <= phi <= upper_phi,
                np.isclose(phi, lower_phi) or np.isclose(phi, upper_phi)
            ]

            if np.any(r_tests) and np.any(phi_tests):
                return (
                    self.coeffs_formula[i](r, self.h_r, self.h_phi, *self.materials),
                    self.initial[i],
                    self.colors[i]
                )
        raise ValueError(f'Unable to assign params for {(r, phi)}')

    def _gen_range(self, r_range, phi_range):
        r_start, r_stop, r_step = r_range
        phi_start, phi_stop, phi_step = phi_range

        h_r = self._validate_step(r_step, 0.01)
        h_phi = self._validate_step(phi_step, 2.0)

        r_vals = np.arange(r_start, r_stop+h_r, h_r)
        phi_vals = np.deg2rad(np.arange(phi_start, phi_stop+h_phi, h_phi))
        return h_r, h_phi, r_vals, phi_vals

    def _gen_base_matrix(self, n_i, n_j):
        return np.array([[None] * n_j] * n_i)

    def _gen_grids(self):
        r_grid, phi_grid = np.meshgrid(self.r_vals, self.phi_vals)
        x_grid = r_grid * np.cos(phi_grid)
        y_grid = r_grid * np.sin(phi_grid)

        meshgrid = np.copy(self.base_matrix)
        for j in range(len(self.r_vals)):
            r = self.r_vals[j]
            for i in range(len(self.phi_vals)):
                phi = self.phi_vals[i]
                coeffs, initial_V, color = self._get_point_params(r, phi)

                meshgrid[i, j]  = Point(
                    (i, j),
                    (r, phi),
                    (initial_V, 0),
                    coeffs,
                    color
                )
        return x_grid, y_grid, meshgrid

    def extract(self, prop):
        prop_matrix = np.copy(self.base_matrix)

        for point in self.meshgrid.ravel():
            if prop == 'color':
                prop_matrix[point.i, point.j] = point.color
            elif prop == 'voltage':
                prop_matrix[point.i, point.j] = point.V
            elif prop == 'temperature':
                raise NotImplementedError
            else:
                raise ValueError(f"Unexpected value '{prop}' passed to `prop`")
        return prop_matrix

    def _plot_meshgrid(self):
        z_grid = np.zeros(self.x_grid.shape)

        data = []
        data.append(
            go.Scatter3d(
                x=self.x_grid.ravel(),
                y=self.y_grid.ravel(),
                z=z_grid.ravel(),
                mode='markers',
                marker=dict(color=self.extract('color').ravel(), size=4)
            )
        )

        line_params   = dict(color='#A3A3A3', width=2)
        for i, j, k in zip(self.x_grid, self.y_grid, z_grid):
            data.append(go.Scatter3d(x=i, y=j, z=k, mode='lines', line=line_params))
        for i, j, k in zip(self.x_grid.T, self.y_grid.T, z_grid.T):
            data.append(go.Scatter3d(x=i, y=j, z=k, mode='lines', line=line_params))
        return go.Figure(data=data)

    def _plot_voltage(self):
        return go.Figure(data=[go.Surface(x=self.x_grid, y=self.y_grid, z=self.extract('voltage'))])

    def _plot_temperature(self):
        raise NotImplementedError

    def plot(self, which):
        which_plot = {
            'meshgrid'    : lambda: self._plot_meshgrid(),
            'voltage'     : lambda: self._plot_voltage(),
            'temperature' : lambda: self._plot_temperature()
        }

        if which not in which_plot.keys():
            raise ValueError(f"Unexpected value '{which}' passed to `which`")

        fig = which_plot[which]()
        fig.show()
        return

    def _overrelaxation(self, lamb, V_curr, V_new):
        return lamb * V_new + (1-lamb) * V_curr

    def _reflex_indexes(self, indexes, max_i, max_j):
        reflected_indexes = []
        for i, j in indexes:
            if i == -1:
                i += 2
            elif i == max_i:
                i -= 2
            else:
                i = i
            if j == -1:
                j += 2
            elif j == max_j:
                j -= 2
            else:
                j = j
            reflected_indexes.append((i,j))
        return reflected_indexes

    def _liebmann_step(self, lamb):
        for i in range(len(self.meshgrid)):
            for j in range(len(self.meshgrid[0])):
                neighbours_voltages = []
                neighbours_indexes = self._reflex_indexes(
                    [(i-1, j), (i, j+1), (i+1, j), (i, j-1)],
                    len(self.meshgrid),
                    len(self.meshgrid[0])
                )

                for idx in neighbours_indexes:
                    neighbours_voltages.append(self.meshgrid[idx].V)

                neighbours_voltages.append(1)
                V_new = self.meshgrid[i, j].update_voltage(np.array(neighbours_voltages))
                self.meshgrid[i, j].V = self._overrelaxation(lamb, self.meshgrid[i, j].V, V_new)

    def _liebamnn_error(self, old, curr):
        return np.max(np.abs(curr - old) / (old + np.finfo(float).tiny))

    def liebmann(self, lamb, epsilon):
        error = np.inf
        step = 0

        while error >= epsilon:
            step += 1
            before = self.extract('voltage')

            self._liebmann_step(lamb)

            error = self._liebamnn_error(before, self.extract('voltage'))
            print(f"Erro máximo: {error}                    ", end='\r')
        print()
        return


class Point:
    def __init__(self, index, cordinates, data, voltage_coeffs, color):
        self.i, self.j = index
        self.r, self.phi = cordinates
        self.V, self.T = data
        self.voltage_coeffs = np.array(voltage_coeffs)
        self.color = color

        self.x = self.r * np.cos(self.phi)
        self.y = self.r * np.sin(self.phi)

    def update_voltage(self, neighbours):
        return np.sum(self.voltage_coeffs * neighbours)

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
