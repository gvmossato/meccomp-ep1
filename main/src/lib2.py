# ============================= #
# Funções de suporte da Parte 2 #
# ============================= #

import numpy as np
import plotly.graph_objs as go
import plotly.figure_factory as ff


class Plate:
    def __init__(self, r_range, phi_range, params, props):
        self.V_params = params['V']
        self.J_params = params['J']
        self.T_params = params['T']
        self.Q_params = params['Q']
        self.M_params = params['M']

        self.i = np.nan
        self.R = np.nan
        self.q_conv = np.nan

        self.h_r, self.h_phi, self.r_vals, self.phi_vals = self._gen_ranges(r_range, phi_range)
        self.n_i, self.n_j = len(self.phi_vals), len(self.r_vals)
        self.x_grid, self.y_grid, self.meshgrid = self._gen_grids()

        self._set_plate_props(props)
        self._points_add_params({
            'M'    : self.M_params,
            'V'    : self.V_params,
            'T'    : self.T_params,
            'Jr'   : self.J_params[0],
            'Jphi' : self.J_params[1],
            'Qr'   : self.Q_params[0],
            'Qphi' : self.Q_params[1],
        })

    def _set_plate_props(self, props):
        for prop, value in props.items():
            exec(f"self.{prop} = {value}")

    def _validate_step(self, h, contour_gcd):
        return contour_gcd / np.round(contour_gcd / h)

    def _gen_ranges(self, r_range, phi_range):
        r_start, r_stop, r_step = r_range
        phi_start, phi_stop, phi_step = phi_range

        h_r = self._validate_step(r_step, 0.01)
        h_phi = self._validate_step(phi_step, 2.0)

        r_vals = np.arange(r_start, r_stop+h_r, h_r)
        phi_vals = np.deg2rad(np.arange(phi_start, phi_stop+h_phi, h_phi))
        return h_r, np.deg2rad(h_phi), r_vals, phi_vals

    def _get_base_matrix(self, element):
        return np.array([[element] * self.n_j] * self.n_i)

    def _get_point_params(self, point, params, is_material=False):
        for i in range(len(params['regions'])):
            lower_r, upper_r, lower_phi, upper_phi = params['regions'][i]

            r_tests = [
                lower_r <= point.r <= upper_r,
                np.isclose(point.r, lower_r) or np.isclose(point.r, upper_r),
            ]
            phi_tests = [
                lower_phi <= point.phi <= upper_phi,
                np.isclose(point.phi, lower_phi) or np.isclose(point.phi, upper_phi)
            ]

            if np.any(r_tests) and np.any(phi_tests):
                if is_material:
                    point_params = {
                        'props'  : params['props'][i],
                        'color'  : params['colors'][i]
                    }
                else:
                    point_params = {
                        'coeffs' : params['coeffs'][i](self, point),
                        'value'  : params['initial'][i],
                        'color'  : params['colors'][i]
                    }
                return point_params
        raise ValueError(f'Unable to assign params for {(point.r, point.phi)}')

    def _gen_grids(self):
        r_grid, phi_grid = np.meshgrid(self.r_vals, self.phi_vals)
        x_grid = r_grid * np.cos(phi_grid)
        y_grid = r_grid * np.sin(phi_grid)

        meshgrid = self._get_base_matrix(None)
        for i in range(self.n_i):
            for j in range(self.n_j):
                meshgrid[i, j] = Point((i, j), (self.r_vals[j], self.phi_vals[i]))
        return x_grid, y_grid, meshgrid

    def _points_add_params(self, map_params):
        for point in self.meshgrid.ravel():
            for param_name, param_dict in map_params.items():
                point.set_param(
                    param_name,
                    self._get_point_params(
                        point,
                        param_dict,
                        param_name == 'M'
                    )
                )
        return

    def get_prop_matrix(self, prop):
        map_props = {
            'M_color'    : lambda p: p.M['color'],
            'V_color'    : lambda p: p.V['color'],
            'T_color'    : lambda p: p.T['color'],
            'Jr_color'   : lambda p: p.J[0]['color'],
            'Jphi_color' : lambda p: p.J[1]['color'],
            'Qr_color'   : lambda p: p.Q[0]['color'],
            'Qphi_color' : lambda p: p.Q[1]['color'],
            'V'          : lambda p: p.V['value'],
            'T'          : lambda p: p.T['value'],
            'Jr'         : lambda p: p.J[0]['value'],
            'Jphi'       : lambda p: p.J[1]['value'],
            'Qr'         : lambda p: p.Q[0]['value'],
            'Qphi'       : lambda p: p.Q[1]['value'],
            'dot_q'      : lambda p: p.dot_q
        }

        if prop not in map_props:
            raise ValueError(f"Unexpected value '{prop}' passed to `prop`")

        prop_matrix = self._get_base_matrix(None) if 'color' in prop else self._get_base_matrix(0.0)
        for point in self.meshgrid.ravel():
            prop_matrix[point.i, point.j] = map_props[prop](point)
        return prop_matrix

    def _calculate_through_wall(self, prop):
        max_r_prop_vals = self.get_prop_matrix(prop)[:, -1].ravel()

        calc = 0
        for i in range(len(max_r_prop_vals)-1):
            calc += (max_r_prop_vals[i] + max_r_prop_vals[i+1]) * self.h_phi / 2

        if prop == 'Jr':
            self.i = 2 * self.r_vals[-1] * calc
        else:
            self.q_conv = 2 * self.r_vals[-1] * calc
        return self.i

    def _calculate_R(self):
        self.R = 100 / self.i
        return self.R

    def calculate_flux(self, prop):
        map_calcs = {
            'J' : lambda: [
                self._calculate_flux_r('Jr', 'V'),
                self._calculate_flux_phi('Jphi', 'V')
            ],
            'Q' : lambda: [
                self._calculate_flux_r('Qr', 'T'),
                self._calculate_flux_phi('Qphi', 'T')
            ],
        }

        if prop not in map_calcs:
            raise ValueError(f"Unexpected value '{prop}' passed to `prop`")
        return map_calcs[prop]()

    def _calculate_flux_r(self, prop, flux_var):
        for i in range(self.n_i):
            for j in range(self.n_j):
                neighbours_vals = []
                neighbours_idxs = [(i, j-2), (i, j-1), (i, j), (i, j+1), (i, j+2)]

                for row_idx, col_idx in neighbours_idxs:
                    if col_idx <= -1 or col_idx >= self.n_j:
                        neighbours_vals.append(0)
                    else:
                        neighbours_vals.append(self.meshgrid[row_idx, col_idx].get(flux_var))

                self.meshgrid[i, j].set(
                    prop,
                    self.meshgrid[i, j].update_and_get(prop, neighbours_vals)
                )
        return

    def _calculate_flux_phi(self, prop, flux_var):
        for i in range(self.n_i):
            for j in range(self.n_j):
                neighbours_vals = []
                neighbours_idxs = [(i+2, j), (i+1, j), (i, j), (i-1, j), (i-2, j)]

                for row_idx, col_idx in neighbours_idxs:
                    if row_idx == -2:
                        neighbours_vals.append(self.meshgrid[row_idx+4, col_idx].get(flux_var))
                    elif row_idx == -1:
                        neighbours_vals.append(self.meshgrid[row_idx+2, col_idx].get(flux_var))
                    elif row_idx >= self.n_i:
                        neighbours_vals.append(0)
                    else:
                        neighbours_vals.append(self.meshgrid[row_idx, col_idx].get(flux_var))

                self.meshgrid[i, j].set(
                    prop,
                    self.meshgrid[i, j].update_and_get(prop, neighbours_vals)
                )
        return

    def _calculate_dot_q(self):
        for point in self.meshgrid.ravel():
            point.dot_q = -(point.get('Jr')**2 + point.get('Jphi')**2) / point.M['props']['sigma']

        self._points_add_params({'T' : self.T_params})
        return

    def calculate(self, prop):
        map_calcs = {
            'dot_q'  : lambda: self._calculate_dot_q(),
            'q_conv' : lambda: self._calculate_through_wall('Qr'),
            'i'      : lambda: self._calculate_through_wall('Jr'),
            'R'      : lambda: self._calculate_R()
        }

        if prop not in map_calcs:
            raise ValueError(f"Unexpected value '{prop}' passed to `prop`")
        return map_calcs[prop]()

    def _mirror_plot(self, grid, invert):
        sign = -1 if invert else 1
        return np.vstack([np.flip(sign*grid), np.flip(grid[1:], axis=1)])

    def _plot_V(self):
        title = "Distribuição de Tensão Elétrica"
        zlabel = "Tensão (V)"

        fig = go.Figure(data = [go.Surface(
            x = self._mirror_plot(self.x_grid, False),
            y = self._mirror_plot(self.y_grid, True),
            z = self._mirror_plot(self.get_prop_matrix('V'), False),
            colorscale = 'Viridis',
        )])
        return fig, title, zlabel

    def _plot_J(self):
        title = "Densidade de Corrente (A/m²)"
        zlabel = ""

        fig = ff.create_quiver(
            self._mirror_plot(self.x_grid, False),
            self._mirror_plot(self.y_grid, True),
            self._mirror_plot(self.get_prop_matrix('Jr'), False),
            self._mirror_plot(self.get_prop_matrix('Jphi'), True),
            scale = 1e-1,
            name = 'quiver',
            line_width = 2,
            line_color = '#32A834'
        )
        return fig, title, zlabel

    def _plot_Q(self):
        title = "Fluxo de Calor (W/m²)"
        zlabel = ""

        fig = ff.create_quiver(
            self._mirror_plot(self.x_grid, False),
            self._mirror_plot(self.y_grid, True),
            self._mirror_plot(self.get_prop_matrix('Qr'), False),
            self._mirror_plot(self.get_prop_matrix('Qphi'), True),
            scale = 1e-1,
            name = 'quiver',
            line_width = 1,
            line_color = '#FC035A'
        )
        return fig, title, zlabel

    def _plot_q_dot(self):
        title = "Distribuição do Calor"
        zlabel = "Potência por volume (W/m³)"

        fig = go.Figure(data = [go.Surface(
            x = self._mirror_plot(self.x_grid, False),
            y = self._mirror_plot(self.y_grid, True),
            z = self._mirror_plot(self.get_prop_matrix('dot_q'), False),
            colorscale = 'Plotly3'
        )])
        return fig, title, zlabel

    def _plot_T(self):
        title = "Distribuição de Temperatura"
        zlabel = "Temperatura (K)"

        fig = go.Figure(data = [go.Surface(
            x = self._mirror_plot(self.x_grid, False),
            y = self._mirror_plot(self.y_grid, True),
            z = self._mirror_plot(self.get_prop_matrix('T'), False),
            colorscale = 'Turbo'
        )])
        return fig, title, zlabel

    def plot(self, which):
        map_plots = {
            'V'     : lambda: self._plot_V(),
            'J'     : lambda: self._plot_J(),
            'Q'     : lambda: self._plot_Q(),
            'dot_q' : lambda: self._plot_q_dot(),
            'T'     : lambda: self._plot_T(),
        }

        if which not in map_plots:
            raise ValueError(f"Unexpected value '{which}' passed to `which`")

        fig, title, zlabel = map_plots[which]()
        fig.update_layout(
            title = title,
            showlegend = False,
            scene = dict(
                xaxis = dict(title="x (m)"),
                yaxis = dict(title="y (m)"),
                zaxis = dict(title=zlabel),
            )
        )
        fig.show()

    def plot_meshgrid(self, which):
        if which not in ['V', 'T', 'Jr', 'Jphi', 'Qr', 'Qphi', 'M']:
            raise ValueError(f"Unexpected value '{which}' passed to `which`")

        mesh_x_grid = self._mirror_plot(self.x_grid, False)
        mesh_y_grid = self._mirror_plot(self.y_grid, True)
        mesh_z_grid = self._mirror_plot(np.zeros(self.x_grid.shape), False)
        mesh_color  = self._mirror_plot(self.get_prop_matrix(f'{which}_color'), False)

        plot_data = []
        plot_data.append(
            go.Scatter3d(
                x = mesh_x_grid.ravel(),
                y = mesh_y_grid.ravel(),
                z = mesh_z_grid.ravel(),
                mode = 'markers',
                showlegend=False,
                marker = dict(color=mesh_color.ravel(), size=4)
            )
        )

        line_style = dict(color='#A3A3A3', width=2)
        for i, j, k in zip(mesh_x_grid, mesh_y_grid, mesh_z_grid):
            plot_data.append(go.Scatter3d(
                x = i,
                y = j,
                z = k,
                mode = 'lines',
                line = line_style,
                hoverinfo = 'none',
                showlegend=False,
            ))
        for i, j, k in zip(mesh_x_grid.T, mesh_y_grid.T, mesh_z_grid.T):
            plot_data.append(go.Scatter3d(
                x = i,
                y = j,
                z = k,
                mode = 'lines',
                line = line_style,
                hoverinfo = 'none',
                showlegend=False,
            ))

        fig = go.Figure(data = plot_data)
        fig.show()
        return

    def apply_liebmann_for(self, which, lamb, max_error):
        liebmann = Liebmann(self, lamb, max_error)
        self.meshgrid = liebmann.solve_for(which)


class Point:
    def __init__(self, index, cordinates):
        self.i, self.j = index
        self.r, self.phi = cordinates

        self.V = None
        self.J = [None, None]
        self.Q = [None, None]
        self.T = None

        self.dot_q = np.nan

    def get(self, prop):
        map_props = {
            'V'    : lambda: self.V['value'],
            'T'    : lambda: self.T['value'],
            'Jr'   : lambda: self.J[0]['value'],
            'Jphi' : lambda: self.J[1]['value'],
            'Qr'   : lambda: self.Q[0]['value'],
            'Qphi' : lambda: self.Q[1]['value']
        }

        if prop not in map_props:
            raise ValueError(f"Unexpected value '{prop}' passed to `prop`")
        return map_props[prop]()

    def set(self, prop, value):
        if prop == 'V':
            self.V['value'] = value
        elif prop == 'T':
            self.T['value'] = value
        elif prop == 'Jr':
            self.J[0]['value'] = value
        elif prop == 'Jphi':
            self.J[1]['value'] = value
        elif prop == 'Qr':
            self.Q[0]['value'] = value
        elif prop == 'Qphi':
            self.Q[1]['value'] = value
        else:
            raise ValueError(f"Unexpected value '{prop}' passed to `prop`")
        return

    def set_param(self, param, value):
        if param == 'V':
            self.V = value
        elif param == 'T':
            self.T = value
        elif param == 'Jr':
            self.J[0] = value
        elif param == 'Jphi':
            self.J[1] = value
        elif param == 'Qr':
            self.Q[0] = value
        elif param == 'Qphi':
            self.Q[1] = value
        elif param == 'M':
            self.M = value
        else:
            raise ValueError(f"Unexpected value '{param}' passed to `param`")
        return

    def update_and_get(self, prop, neighbours):
        map_props = {
            'V'    : lambda neigh: np.sum(self.V['coeffs'] * neigh),
            'T'    : lambda neigh: np.sum(self.T['coeffs'] * neigh),
            'Jr'   : lambda neigh: np.sum(self.J[0]['coeffs'] * neigh),
            'Jphi' : lambda neigh: np.sum(self.J[1]['coeffs'] * neigh),
            'Qr'   : lambda neigh: np.sum(self.J[0]['coeffs'] * neigh),
            'Qphi' : lambda neigh: np.sum(self.J[1]['coeffs'] * neigh)
        }

        if prop not in map_props:
            raise ValueError(f"Unexpected value '{prop}' passed to `prop`")
        return map_props[prop](np.array(neighbours))


class Liebmann:
    def __init__(self, plate, lamb, max_error):
        self.plate = plate
        self.lamb = lamb
        self.epsilon = max_error
        self.step_count = 0

    def _SOR(self, V_new, V_curr):
        return self.lamb * V_new + (1-self.lamb) * V_curr

    def _get_error(self, old, curr):
        return np.max(np.abs(curr - old) / (curr + np.finfo(float).tiny))

    def _next_step(self, prop):
        meshgrid = self.plate.meshgrid

        n_rows = len(meshgrid)
        n_cols = len(meshgrid[0])

        for i in range(n_rows):
            for j in range(n_cols):
                neighbours_vals  = []
                neighbours_idxs = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]

                for row_idx, col_idx in neighbours_idxs:
                    if row_idx == -1:
                        neighbours_vals.append(meshgrid[row_idx+2, col_idx].get(prop))
                    elif col_idx == -1 or row_idx == n_rows or col_idx == n_cols:
                        neighbours_vals.append(0)
                    else:
                        neighbours_vals.append(meshgrid[row_idx, col_idx].get(prop))

                neighbours_vals.append(1)

                prop_updated_val = meshgrid[i, j].update_and_get(prop, np.array(neighbours_vals))
                prop_new_val = self._SOR(prop_updated_val, meshgrid[i, j].get(prop))
                meshgrid[i, j].set(prop, prop_new_val)
        return

    def solve_for(self, prop):
        error = np.inf

        while error >= self.epsilon:
            self.step_count += 1
            before = self.plate.get_prop_matrix(prop)
            self._next_step(prop)
            error = self._get_error(before, self.plate.get_prop_matrix(prop))
            print(f"Erro máximo: {error}                ", end='\r')

        print()
        return self.plate.meshgrid
