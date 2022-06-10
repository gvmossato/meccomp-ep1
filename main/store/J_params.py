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
    lambda P, p: [ # Vermelho
        0.0,
        0.0,
        3*p.sa / (2*P.dr),
        -2*p.sa / P.dr,
        p.sa / (2*P.dr)
    ],
    lambda P, p: [ # Azul
        0.0,
        0.0,
        3*p.sb / (2*P.dr),
        -2*p.sb / P.dr,
        p.sb / (2*P.dr)
    ],
    lambda P, p: [ # Verde
        -p.sb / (2*P.dr),
        2*p.sb / P.dr,
        -3*p.sb / (2*P.dr),
        0.0,
        0.0
    ],
    lambda P, p: [ # Rosa
        -p.sa / (2*P.dr),
        2*p.sa / P.dr,
        -3*p.sa / (2*P.dr),
        0.0,
        0.0
    ],
    lambda P, p: [ # Roxo
        0.0,
        p.sb / (2*P.dr),
        0.0,
        -p.sb / (2*P.dr),
        0.0
    ],
    lambda P, p: [ # Cinza
        0.0,
        p.sa / (2*P.dr),
        0.0,
        -p.sa / (2*P.dr),
        0.0
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
    lambda P, p: [ # Roxo
        0.0,
        0.0,
        -3*p.sb / (2*P.dp*p.r),
        2*p.sb / (P.dp*p.r),
        -p.sb / (2*P.dp*p.r)
    ],
    lambda P, p: [ # Laranja
        0.0,
        0.0,
        -3*p.sa / (2*P.dp*p.r),
        2*p.sa / (P.dp*p.r),
        -p.sa / (2*P.dp*p.r)
    ],
    lambda P, p: [ # Azul
        0.0,
        -p.sb / (2*P.dp*p.r),
        0.0,
        p.sb / (2*P.dp*p.r),
        0.0
    ],
    lambda P, p: [ # Cinza
        0.0,
        -p.sa / (2*P.dp*p.r),
        0.0,
        p.sa / (2*P.dp*p.r),
        0.0
    ]
]

phi_initial = [
    0.0, # Roxo
    0.0, # Laranja
    0.0, # Azul
    0.0  # Cinza
]

phi_colors = [
    "#9000FF", # Roxo
    "#FF6000", # Laranja
    "#0000FF", # Azul
    "#A7A7A7"  # Cinza
]

# ========= #
# Materiais #
# ========= #

materials_colormap = {
    "#9000FF" : (1.0e-5, 500), # Roxo
    "#FF6000" : (0.5e-5, 110), # Laranja
    "#0000FF" : (1.0e-5, 110), # Azul
    "#A7A7A7" : (0.5e-5, 500)  # Cinza
}
