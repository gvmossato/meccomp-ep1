# ====================== #
# Parâmetros de material #
# ====================== #

import numpy as np


regions = np.array([
    [   0.05,   0.08,    00.0,   18.0], # Amarelo
    [-np.inf, np.inf, -np.inf, np.inf]  # Cinza
])
regions[:, -2:] = np.deg2rad(regions[:, -2:])

props = [
    {
        'sigma' :  1e-5,
        'k' : 500
    },
    {
        'sigma' : 5e-6,
        'k' : 110
    }
]

colors = [
    "#FFCC00", # Amarelo
    "#A7A7A7"  # Cinza
]
