import main.store.M_params as M
import main.store.V_params as V
import main.store.J_params as J
import main.store.T_params as T
import main.store.Q_params as Q


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

params = {
    'V' : voltage_params,
    'J' : current_density_params,
    'T' : temperature_params,
    'Q' : heat_flux_params,
    'M' : materials_params
}
