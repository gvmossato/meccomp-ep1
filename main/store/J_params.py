import numpy as np

# ==== #
# Raio #
# ==== #

r_regions = np.array([
    [   0.03,   0.03,     0.0,   40.0], # Vermelho
    [   0.05,   0.05,     0.0,   18.0], # Azul
    [   0.08,   0.08,     0.0,   18.0], # Verde
    [   0.11,   0.11,     0.0,   40.0], # Rosa
    [   0.05,   0.08,     0.0,   18.0], # Roxo
    [-np.inf, np.inf, -np.inf, np.inf]  # Cinza
])
r_regions[:, -2:] = np.deg2rad(r_regions[:, -2:])

r_coeffs = [
    lambda r, dr, dp, sa, sb: [ # Vermelho
        0.0,
        0.0,
        -3*sa / (2*dr),
        2*sa / dr,
        -sa / (2*dr)
    ],
    lambda r, dr, dp, sa, sb: [ # Azul
        0.0,
        0.0,
        -3*sb / (2*dr),
        2*sb / dr,
        -sb / (2*dr)
    ],
    lambda r, dr, dp, sa, sb: [ # Verde
        sb / (2*dr),
        -2*sb / dr,
        3*sb / (2*dr),
        0.0,
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Rosa
        sa / (2*dr),
        -2*sa / dr,
        3*sa / (2*dr),
        0.0,
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Roxo
        0
        -sb / (2*dr),
        0.0,
        sb / (2*dr),
        0.0,
    ],
    lambda r, dr, dp, sa, sb: [ # Cinza
        0
        -sa / (2*dr),
        0.0,
        sa / (2*dr),
        0.0,
    ]
]

r_initial = [
    0.0, # Vermelho
    0.0, # Azul
    0.0, # Verde
    0.0, # Rosa
    0.0, # Roxo
    0.0  # Cinza
]

r_colors = [
    "#FF0000", # Vermelho
    "#0000FF", # Azul
    "#00FF00", # Verde
    "#FF0070", # Rosa
    "#9000FF", # Roxo
    "#A7A7A7"  # Cinza
]

# ====== #
# Ângulo #
# ====== #

phi_regions = np.array([
    [   0.05,   0.08,    18.0,   18.0], # Roxo
    [   0.03,   0.11,    40.0,   40.0], # Laranja
    [   0.05,   0.08,    00.0,   18.0], # Azul
    [-np.inf, np.inf, -np.inf, np.inf]  # Cinza
])
phi_regions[:, -2:] = np.deg2rad(phi_regions[:, -2:])

phi_coeffs = [
    lambda r, dr, dp, sa, sb: [ # Roxo
        sb / (2*dp*r),
        -2*sb / (dp*r),
        3*sb / (2*dp*r),
        0.0,
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Laranja
        sa / (2*dp*r),
        -2*sa / (dp*r),
        3*sa / (2*dp*r),
        0.0,
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Azul
        0
        -sb / (2*dp*r),
        0.0,
        sb / (2*dp*r),
        0.0,
    ],
    lambda r, dr, dp, sa, sb: [ # Cinza
        0
        -sa / (2*dp*r),
        0.0,
        sa / (2*dp*r),
        0.0,
    ]
]

phi_initial = [
    0.0, # Vermelho
    0.0, # Azul
    0.0, # Verde
    0.0, # Rosa
    0.0, # Roxo
    0.0  # Cinza
]

phi_colors = [
    "#FF6000", # Laranja
    "#9000FF", # Roxo
    "#0000FF", # Azul
    "#A7A7A7"  # Cinza
]
