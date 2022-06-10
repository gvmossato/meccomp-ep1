import numpy as np


regions = np.array([
    [   0.03,   0.03,    00.0,   40.0], # Vermelho
    [   0.05,   0.05,    00.0,   18.0], # Azul
    [   0.08,   0.08,    00.0,   18.0], # Verde
    [   0.11,   0.11,    00.0,   40.0], # Rosa
    [   0.05,   0.08,    18.0,   18.0], # Roxo
    [   0.03,   0.11,    40.0,   40.0], # Laranja
    [   0.05,   0.08,    00.0,   18.0], # Amarelo
    [-np.inf, np.inf, -np.inf, np.inf]  # Cinza
])
regions[:, -2:] = np.deg2rad(regions[:, -2:])

coeffs = [
    lambda P, p: [ # Vermelho
        0.0,
        0.0,
        0.0,
        0.0,
      303.0
    ],
    lambda P, p: [ # Azul
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.kb * p.r**2 * (2*p.r + P.h_r) / ( (P.h_phi**2 * p.r**2 + P.h_r**2) * (P.h_r * (p.kb-p.ka) + 2*p.r*(p.ka+p.kb)) ),
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.ka * p.r**2 * (2*p.r - P.h_r) / ( (P.h_phi**2 * p.r**2 + P.h_r**2) * (P.h_r * (p.kb-p.ka) + 2*p.r*(p.ka+p.kb)) ),
        2*p.dotq * P.h_phi**2 * P.h_r**2 * p.r**3 / ( (P.h_phi**2 * p.r**2 + P.h_r**2) * (P.h_r * (p.kb-p.ka) + 2*p.r*(p.ka+p.kb)) )
    ],
    lambda P, p: [ # Verde
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.ka * p.r**2 * (2*p.r + P.h_r) / ( (P.h_phi**2 * p.r**2 + P.h_r**2) * (P.h_r * (p.ka-p.kb) + 2*p.r*(p.ka+p.kb)) ),
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.kb * p.r**2 * (2*p.r - P.h_r) / ( (P.h_phi**2 * p.r**2 + P.h_r**2) * (P.h_r * (p.ka-p.kb) + 2*p.r*(p.ka+p.kb)) ),
        2*p.dotq * P.h_phi**2 * P.h_r**2 * p.r**3 / ( (P.h_phi**2 * p.r**2 + P.h_r**2) * (P.h_r * (p.ka-p.kb) + 2*p.r*(p.ka+p.kb)) )
    ],
    lambda P, p: [ # Rosa
        P.h_r**2 * p.ka / ( 2*P.h_phi * p.r * (P.h_r**2 * p.h + 2*P.h_r * p.h * p.r + 2*p.ka * p.r) ),
        0.0,
        -P.h_r**2 * p.ka / ( 2*P.h_phi * p.r * (P.h_r**2 * p.h + 2*P.h_r * p.h * p.r + 2*p.ka * p.r) ),
        2*p.ka * p.r / ( P.h_r**2 * p.h + 2*P.h_r * p.h * p.r + 2*p.ka * p.r ),
        ( p.dotq * P.h_r**2 * p.r + p.Tamb * P.h_r * p.h * (P.h_r + 2*p.r) ) / ( P.h_r**2 * p.h + 2*P.h_r * p.h * p.r + 2*p.ka * p.r )
    ],
    lambda P, p: [ # Roxo
        P.h_r**2 * p.ka / ( (p.ka+p.kb) * (P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.r * (P.h_r  + 2*p.r) / ( 4*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_r**2 * p.kb / ( (p.ka+p.kb) * (P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.r * (-P.h_r + 2*p.r) / ( 4*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        p.dotq * P.h_phi**2 * P.h_r**2 * p.r**2 / ( (p.ka+p.kb) * (P.h_phi**2 * p.r**2 + P.h_r**2) ),
    ],
    lambda P, p: [ # Laranja
        0.0,
        ( 2*p.r + P.h_r ) / ( 4*p.r ),
        0.0,
        ( 2*p.r - P.h_r ) / ( 4*p.r ),
        p.dotq * P.h_r**2 / ( 2*p.ka )
    ],
    lambda P, p: [ # Amarelo
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.r * (2*p.r + P.h_r) / ( 4*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.r * (2*p.r - P.h_r) / ( 4*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        p.dotq * P.h_phi**2 * P.h_r**2 * p.r**2 / ( 2*p.kb * (P.h_phi**2 * p.r**2 + P.h_r**2) )
    ],
    lambda P, p: [ # Cinza
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.r * (2*p.r + P.h_r) / ( 4*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_r**2 / ( 2*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        P.h_phi**2 * p.r * (2*p.r - P.h_r) / ( 4*(P.h_phi**2 * p.r**2 + P.h_r**2) ),
        p.dotq * P.h_phi**2 * P.h_r**2 * p.r**2 / ( 2*p.ka * (P.h_phi**2 * p.r**2 + P.h_r**2) )
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
