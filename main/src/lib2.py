import numpy as np
import plotly.graph_objs as go


class Plate:
    def __init__(self, r_range, phi_range, params, materials):
        self.V_params = params['voltage']
        self.J_params = params['current_density']
        self.materials = materials

        self.h_r, self.h_phi, self.r_vals, self.phi_vals = self._gen_ranges(r_range, phi_range)
        self.base_matrix = self._gen_base_matrix(len(self.phi_vals), len(self.r_vals))
        self.x_grid, self.y_grid, self.meshgrid = self._gen_grids()

    def _validate_step(self, h: float, contour_gcd: float):
        return contour_gcd / np.round(contour_gcd / h)

    def _get_point_params(self, r, phi, params):
        for i in range(len(params['regions'])):
            lower_r, upper_r, lower_phi, upper_phi = params['regions'][i]

            r_tests = [
                lower_r <= r <= upper_r,
                np.isclose(r, lower_r) or np.isclose(r, upper_r),
            ]
            phi_tests = [
                lower_phi <= phi <= upper_phi,
                np.isclose(phi, lower_phi) or np.isclose(phi, upper_phi)
            ]

            if np.any(r_tests) and np.any(phi_tests):
                args = [r, self.h_r, self.h_phi, *self.materials]
                point_params = {
                    'coeffs' : params['coeffs'][i](*args),
                    'value'  : params['initial'][i],
                    'color'  : params['colors'][i]
                }
                return point_params
        raise ValueError(f'Unable to assign params for {(r, phi)}')

    def _gen_ranges(self, r_range, phi_range):
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

                V_params_point = self._get_point_params(r, phi, self.V_params)
                Jr_params_point = self._get_point_params(r, phi, self.J_params[0])
                Jphi_params_point = self._get_point_params(r, phi, self.J_params[1])

                meshgrid[i, j]  = Point(
                    (i, j),
                    (r, phi),
                    V_params_point,
                    (Jr_params_point, Jphi_params_point)
                )
        return x_grid, y_grid, meshgrid

    def get_prop(self, prop):
        prop_matrix = np.copy(self.base_matrix)

        if prop == 'V_color':
            for point in self.meshgrid.ravel():
                prop_matrix[point.i, point.j] = point.V['color']

        elif prop == 'Jr_color':
            for point in self.meshgrid.ravel():
                prop_matrix[point.i, point.j] = point.J[0]['color']

        elif prop == 'Jphi_color':
            for point in self.meshgrid.ravel():
                prop_matrix[point.i, point.j] = point.J[1]['color']

        elif prop == 'voltage':
            for point in self.meshgrid.ravel():
                prop_matrix[point.i, point.j] = point.V['value']

        else:
            raise ValueError(f"Unexpected value '{prop}' passed to `prop`")
        return prop_matrix

    def plot(self, which):
        if which == 'voltage':
            fig = go.Figure(data = [go.Surface(
                x = self.x_grid,
                y = self.y_grid,
                z = self.get_prop('voltage')
            )])
            fig.show()


    def plot_meshgrid(self, which):
        if which not in ['V', 'Jr', 'Jphi']:
            raise ValueError(f"Unexpected value '{which}' passed to `which`")

        z_grid = np.zeros(self.x_grid.shape)
        plot_data = []

        plot_data.append(
            go.Scatter3d(
                x = self.x_grid.ravel(),
                y = self.y_grid.ravel(),
                z = z_grid.ravel(),
                mode = 'markers',
                marker = dict(color=self.get_prop(f'{which}_color').ravel(), size=4)
            )
        )

        line_style = dict(color='#A3A3A3', width=2)
        for i, j, k in zip(self.x_grid, self.y_grid, z_grid):
            plot_data.append(go.Scatter3d(
                x = i,
                y = j,
                z = k,
                mode = 'lines',
                line = line_style
            ))
        for i, j, k in zip(self.x_grid.T, self.y_grid.T, z_grid.T):
            plot_data.append(go.Scatter3d(
                x = i,
                y = j,
                z = k,
                mode = 'lines',
                line = line_style
            ))

        fig = go.Figure(data = plot_data)
        fig.show()
        return

    def apply_liebmman_for(self, lamb, max_error, which='voltage'):
        liebmann = Liebmann(self, lamb, max_error)
        self.meshgrid = liebmann.solve_for(which)


class Point:
    def __init__(self, index, cordinates, V_params, J_params):
        self.i, self.j = index
        self.r, self.phi = cordinates
        self.V = V_params
        self.J = J_params

    def update_voltage(self, neighbours):
        return np.sum(self.V['coeffs'] * neighbours)


class Liebmann:
    def __init__(self, plate, lamb, max_error):
        self.plate = plate
        self.lamb = lamb
        self.epsilon = max_error
        self.step_count = 0

    def _SOR(self, V_new, V_curr):
        return self.lamb * V_new + (1-self.lamb) * V_curr

    def _next_step(self):
        meshgrid = self.plate.meshgrid

        n_rows = len(meshgrid)
        n_cols = len(meshgrid[0])

        for i in range(n_rows):
            for j in range(n_cols):
                neighbours_values  = []
                neighbours_indexes = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]

                for row_idx, col_idx in neighbours_indexes:
                    if row_idx == -1:
                        neighbours_values.append(meshgrid[row_idx+2, col_idx].V['value'])
                    elif col_idx == -1 or row_idx == n_rows or col_idx == n_cols:
                        neighbours_values.append(0)
                    else:
                        neighbours_values.append(meshgrid[row_idx, col_idx].V['value'])

                neighbours_values.append(1)

                V_new = meshgrid[i, j].update_voltage(np.array(neighbours_values))
                meshgrid[i, j].V['value'] = self._SOR(V_new, meshgrid[i, j].V['value'])

    def _get_error(self, old, curr):
        return np.max(np.abs(curr - old) / (curr + np.finfo(float).tiny))

    def solve_for(self, prop='voltage'):
        error = np.inf

        while error >= self.epsilon:
            self.step_count += 1
            before = self.plate.get_prop('voltage')
            self._next_step()
            error = self._get_error(before, self.plate.get_prop('voltage'))
            print(f"Erro máximo: {error}                ", end='\r')

        print()
        return self.plate.meshgrid
