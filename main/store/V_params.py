import numpy as np


regions = np.array([
    [   0.03,   0.03,    00.0,   40.0], # Vermelho
    [   0.05,   0.05,    00.0,   18.0], # Azul
    [   0.08,   0.08,    00.0,   18.0], # Verde
    [   0.11,   0.11,    00.0,   40.0], # Rosa
    [   0.05,   0.08,    18.0,   18.0], # Roxo
    [   0.03,   0.11,    40.0,   40.0], # Laranja
    [-np.inf, np.inf, -np.inf, np.inf]  # Cinza
])
regions[:, -2:] = np.deg2rad(regions[:, -2:])

coeffs = [
    lambda P, p: [ # Vermelho
        0.0,
        0.0,
        0.0,
        0.0,
        100.0
    ],
    lambda P, p: [ # Azul
        ( P.dr**2 ) / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.sb * p.r**2 * (P.dr  + 2*p.r) ) / ( (P.dp**2 * p.r**2 + P.dr**2) * (P.dr * (p.sb-p.sa) + 2*p.r*(p.sa+p.sb)) ),
        ( P.dr**2 ) / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.sa * p.r**2 * (-P.dr + 2*p.r) ) / ( (P.dp**2 * p.r**2 + P.dr**2) * (P.dr * (p.sb-p.sa) + 2*p.r*(p.sa+p.sb)) ),
        0.0
    ],
    lambda P, p: [ # Verde
        ( P.dr**2 ) / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.sa * p.r**2 * (P.dr  + 2*p.r) ) / ( (P.dp**2 * p.r**2 + P.dr**2) * (P.dr * (p.sa-p.sb) + 2*p.r*(p.sa+p.sb)) ),
        ( P.dr**2 ) / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.sb * p.r**2 * (-P.dr + 2*p.r) ) / ( (P.dp**2 * p.r**2 + P.dr**2) * (P.dr * (p.sa-p.sb) + 2*p.r*(p.sa+p.sb)) ),
        0.0
    ],
    lambda P, p: [ # Rosa
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    lambda P, p: [ # Roxo
        ( P.dr**2 * p.sa ) / ( (p.sa+p.sb) * (P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.r * (P.dr  + 2*p.r) ) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dr**2 * p.sb ) / ( (p.sa+p.sb) * (P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.r * (-P.dr + 2*p.r) ) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        0.0
    ],
    lambda P, p: [ # Laranja
        0.0,
        ( P.dp**2 * p.r * (P.dr  + 2*p.r) ) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dr**2 ) / ( P.dp**2 * p.r**2 + P.dr**2 ),
        ( P.dp**2 * p.r * (-P.dr + 2*p.r) ) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        0.0
    ],
    lambda P, p: [ # Cinza
        ( P.dr**2 ) / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.r * (P.dr  + 2*p.r) ) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dr**2 ) / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        ( P.dp**2 * p.r * (-P.dr + 2*p.r) ) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        0.0
    ]
]

initial = [
    100.0, # Vermelho
      0.0, # Azul
      0.0, # Verde
      0.0, # Rosa
      0.0, # Roxo
      0.0, # Laranja
      0.0  # Cinza
]

colors = [
    "#FF0000", # Vermelho
    "#0000FF", # Azul
    "#00FF00", # Verde
    "#FF0070", # Rosa
    "#9000FF", # Roxo
    "#FF6000", # Laranja
    "#A7A7A7"  # Cinza
]
