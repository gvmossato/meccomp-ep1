import numpy as np


regions = np.array([
    [   0.03,   0.11,    40.0,   40.0], # Laranja
    [   0.05,   0.08,    00.0,   18.0], # Amarelo
    [-np.inf, np.inf, -np.inf, np.inf]  # Cinza
])
regions[:, -2:] = np.deg2rad(regions[:, -2:])

coeffs = [
    lambda P, p: [ # Laranja
        0.0,
        ( 2*p.r + P.dr ) / ( 4*p.r ),
        0.0,
        ( 2*p.r - P.dr ) / ( 4*p.r ),
        p.dotq * P.dr**2 / ( 2*P.ka )
    ],
    lambda P, p: [ # Amarelo
        P.dr**2 / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        P.dp**2 * p.r * (2*p.r + P.dr) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        P.dr**2 / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        P.dp**2 * p.r * (2*p.r - P.dr) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        p.dotq * P.dp**2 * P.dr**2 * p.r**2 / ( 2*p.kb * (P.dp**2 * p.r**2 + P.dr**2) )
    ],
    lambda P, p,: [ # Cinza
        P.dr**2 / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        P.dp**2 * p.r * (2*p.r + P.dr) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        P.dr**2 / ( 2*(P.dp**2 * p.r**2 + P.dr**2) ),
        P.dp**2 * p.r * (2*p.r - P.dr) / ( 4*(P.dp**2 * p.r**2 + P.dr**2) ),
        p.dotq * P.dp**2 * P.dr**2 * p.r**2 / ( 2*P.ka * (P.dp**2 * p.r**2 + P.dr**2) )
    ]
]

initial = [
    303.0, # Vermelho
      0.0, # Azul
      0.0, # Verde
      0.0, # Rosa
      0.0, # Roxo
      0.0, # Laranja
      0.0, # Amarelo
      0.0  # Cinza
]

colors = [
    "#FF0000", # Vermelho
    "#0000FF", # Azul
    "#00FF00", # Verde
    "#FF0070", # Rosa
    "#9000FF", # Roxo
    "#FF6000", # Laranja
    "#FFCC00", # Amarelo
    "#A7A7A7"  # Cinza
]
