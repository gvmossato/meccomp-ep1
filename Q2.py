import numpy as np

from EPLib import Plate


def gray(point, neigh_temps, equations):
    coeffs = equations[:-1]
    denominator = equations[-1]

    numerator = coeffs * neigh_temps
    return numerator / denominator


global p, sig_a, sig_b

r_range = [0.03, 0.11, 0.001]
phi_range = [0.0, 40.0, 1.0]

p = Plate(r_range, phi_range)

regions = [
    [     (0.03, 0.03),      (00.0, 40.0)], # Vermelho
    [     (0.05, 0.05),      (00.0, 18.0)], # Azul
    [     (0.08, 0.08),      (00.0, 18.0)], # Verde
    [     (0.11, 0.11),      (00.0, 40.0)], # Rosa
    [     (0.03, 0.11),      (40.0, 40.0)], # Roxo
    [     (0.05, 0.08),      (18.0, 18.0)], # Laranja
    [(-np.inf, np.inf), (-np.inf, np.inf)]  # Cinza
]
regions = np.deg2rad(regions[:, 1])

equations = [
    lambda r: [ # Vermelho
        0,
        0,
        0,
        0,
        np.inf
    ],
    lambda r: [ # Azul
        -p.delta_r**3 * sig_a + p.delta_r**3 * sig_b + 2 * p.delta_r**2 * sig_a * r + 2 * p.delta_r**2 * sig_b * r,
        2 * p.delta_phi**2 * p.delta_r * sig_b * r**2 + 4 * p.delta_phi**2 * sig_b * r**3,
        -p.delta_r**3 * sig_a + p.delta_r**3 * sig_b + 2 * p.delta_r**2 * sig_a * r + 2 * p.delta_r**2 * sig_b * r,
        -2 * p.delta_phi**2 * p.delta_r * sig_a * r**2 + 4 * p.delta_phi**2 * sig_a * r**3,
        2 * (p.delta_phi**2 * r**2 + p.delta_r**2) * (p.delta_r * sig_a - p.delta_r * sig_b - 2 * sig_a * r - 2 * sig_b * r)
    ],
    lambda r: [ # Verde
        p.delta_r**3 * sig_a - p.delta_r**3 * sig_b + 2 * p.delta_r**2 * sig_a * r + 2 * p.delta_r**2 * sig_b * r,
        2 * p.delta_phi**2 * p.delta_r * sig_a * r**2 + 4 * p.delta_phi**2 * sig_a * r**3,
        p.delta_r**3 * sig_a - p.delta_r**3 * sig_b + 2 * p.delta_r**2 * sig_a * r + 2 * p.delta_r**2 * sig_b * r,
        -2 * p.delta_phi**2 * p.delta_r * sig_b * r**2 + 4 * p.delta_phi**2 * sig_b * r**3,
        2 * (p.delta_phi**2 * r**2 + p.delta_r**2) * (p.delta_r * sig_a - p.delta_r * sig_b + 2 * sig_a * r + 2 * sig_b * r)
    ],
    lambda r: [ # Rosa
        0,
        0,
        0,
        0,
        np.inf
    ],
    lambda r: [ # Roxo
        4 * p.delta_r**2 * sig_b,
        p.delta_phi**2 * p.delta_r * sig_a * r + p.delta_phi**2 * p.delta_r * sig_b * r + 2 * p.delta_phi**2 * sig_a * r**2 + 2 * p.delta_phi**2 * sig_b * r**2,
        4 * p.delta_r**2 * sig_a,
        -p.delta_phi**2 * p.delta_r * sig_a * r - p.delta_phi**2 * p.delta_r * sig_b * r + 2 * p.delta_phi**2 * sig_a * r**2 + 2 * p.delta_phi**2 * sig_b * r**2,
        4 * (sig_a + sig_b) * (p.delta_phi**2 * r**2 + p.delta_r**2)
    ],
    lambda r: [ # Laranja
        0,
        p.delta_phi**2 * p.delta_r * r + 2 * p.delta_phi**2 * r**2,
        4 * p.delta_r**2,
        -p.delta_phi**2 * p.delta_r * r + 2 * p.delta_phi**2 * r**2,
        4 * (p.delta_phi**2 * r**2 + p.delta_r**2)
    ]
]

p.add_boundaries(regions, equations)

print(f'meshgrid finalizada! {p.meshgrid.shape}')

p.plot('meshgrid')
