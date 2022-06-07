import numpy as np
import plotly.graph_objs as go


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
        return h_r, np.deg2rad(h_phi), r_vals, phi_vals

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

    def _liebmann_step(self, lamb):
        for i in range(len(self.meshgrid)):
            for j in range(len(self.meshgrid[0])):
                neighbours_voltages = []
                neighbours_indexes = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]

                for row, col in neighbours_indexes:
                    if row == -1:
                        neighbours_voltages.append(self.meshgrid[row+2, col].V)
                    elif col == -1 or row == len(self.meshgrid) or col == len(self.meshgrid[0]):
                        neighbours_voltages.append(0)
                    else:
                        neighbours_voltages.append(self.meshgrid[row, col].V)

                neighbours_voltages.append(1)
                V_new = self.meshgrid[i, j].update_voltage(np.array(neighbours_voltages))
                self.meshgrid[i, j].V = self._overrelaxation(lamb, self.meshgrid[i, j].V, V_new)

    def _liebamnn_error(self, old, curr):
        return np.max(np.abs(curr - old) / (curr + np.finfo(float).tiny))

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

        #print(self.color, self.voltage_coeffs)

        self.x = self.r * np.cos(self.phi)
        self.y = self.r * np.sin(self.phi)

    def update_voltage(self, neighbours):
        return np.sum(self.voltage_coeffs * neighbours)
