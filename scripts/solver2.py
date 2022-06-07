import numpy as np
import store.V_params as V

from src.lib2 import Plate




params = {
    'regions' : V.regions,
    'coeffs'  : V.coeffs,
    'initial' : V.initial,
    'colors'  : V.colors
}

materials = [5e-1, 1]

r_range = [0.03, 0.11, 0.001]
phi_range = [0.0, 40.0, 1.0]

plate = Plate(r_range, phi_range, params, materials)

plate.liebmann(1.75, 0.001)

plate.plot('meshgrid')

plate.plot('voltage')
