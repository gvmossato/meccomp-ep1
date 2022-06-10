import numpy as np
import store.M_params as M
import store.V_params as V
import store.J_params as J
import store.T_params as T
import store.Q_params as Q

from src.lib2 import Plate


r_range = [0.03, 0.11, 0.001]
phi_range = [0.0, 40.0, 1.0]

props = {
    'sa'   : 5e-6,
    'sb'   : 1e-5,
    'ka'   : 110.0,
    'kb'   : 500.0,
    'Tamb' : 298.0,
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

heat_flux_params = (
    {
        'regions' : Q.r_regions,
        'coeffs'  : Q.r_coeffs,
        'initial' : Q.r_initial,
        'colors'  : Q.r_colors
    },
    {
        'regions' : Q.phi_regions,
        'coeffs'  : Q.phi_coeffs,
        'initial' : Q.phi_initial,
        'colors'  : Q.phi_colors
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
    'Q' : heat_flux_params,
    'M' : materials_params
}

plate = Plate(r_range, phi_range, params, props)

print('Meshgrid inicializada!')

plate.plot_meshgrid('M')

plate.plot_meshgrid('V')

plate.plot_meshgrid('Jr')

plate.plot_meshgrid('Jphi')

plate.plot_meshgrid('Qr')

plate.plot_meshgrid('Qphi')

print('Meshgrids plotadas!')

plate.apply_liebmann_for('V', 1.75, 0.001)

print('Tensão calculada!')

plate.plot('V')

plate.calculate('J')

print('Densidade de corrente calculada!')

plate.plot('J')

print('Densidade de corrente plotada!')

plate.calculate('dot_q')

print('Calor distribuído calculado!')

plate.plot('dot_q')

plate.apply_liebmann_for('T', 1.75, 0.001)

print('Temperatura calculada!')

plate.plot('T')

plate.calculate('Q')

plate.plot('Q')
