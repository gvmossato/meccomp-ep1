import numpy as np
import store.M_params as M
import store.V_params as V
import store.J_params as J
import store.T_params as T

from src.lib2 import Plate


r_range = [0.03, 0.11, 0.001]
phi_range = [0.0, 40.0, 1.0]

props = {
    'sa'   : 5e-6,
    'sb'   : 1e-5,
    'ka'   : 110.0,
    'kb'   : 500.0,
    'Tamb' : 303.0,
    'h'    : 50.0
}

materials_params = {
    'regions' : M.regions,
    'props'   : M.props,
    'colors'  : M.colors
}

voltage_params = {
    'regions' : V.regions,
    'coeffs'  : V.coeffs,
    'initial' : V.initial,
    'colors'  : V.colors
}

current_density_params = (
    {
        'regions' : J.r_regions,
        'coeffs'  : J.r_coeffs,
        'initial' : J.r_initial,
        'colors'  : J.r_colors
    },
    {
        'regions' : J.phi_regions,
        'coeffs'  : J.phi_coeffs,
        'initial' : J.phi_initial,
        'colors'  : J.phi_colors
    }
)

temperature_params = {
    'regions' : T.regions,
    'coeffs'  : T.coeffs,
    'initial' : T.initial,
    'colors'  : T.colors
}

params = {
    'V' : voltage_params,
    'J' : current_density_params,
    'T' : temperature_params,
    'M' : materials_params
}

plate = Plate(r_range, phi_range, params, props)

plate.plot_meshgrid('M')

# #plate.plot_meshgrid('V')

# #plate.plot_meshgrid('Jr')

# #plate.plot_meshgrid('Jphi')

# plate.apply_liebmman_for('voltage', 1.75, 0.001)

# plate.plot('voltage')

# plate.calculate('J', J.materials_colormap)

# plate.calculate('dot_q', J.materials_colormap)

# # plate.plot('J')

# plate.plot('dot_q')

# plate.apply_liebmman_for('temperature', 1.75, 0.001)

# plate.plot('temperature')
