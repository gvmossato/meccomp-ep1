import numpy as np

from EPLib import Plate


regions = np.array([
    [   0.03,   0.03,    00.0,   40.0], # Vermelho
    [   0.05,   0.05,    00.0,   18.0], # Azul
    [   0.08,   0.08,    00.0,   18.0], # Verde
    [   0.11,   0.11,    00.0,   40.0], # Rosa
    [   0.03,   0.11,    40.0,   40.0], # Roxo
    [   0.05,   0.08,    18.0,   18.0], # Laranja
    [-np.inf, np.inf, -np.inf, np.inf]  # Cinza
])
regions[:, -2:] = np.deg2rad(regions[:, -2:])

coeffs = [
    lambda r, dr, dp, sa, sb: [ # Vermelho
        0.0,
        0.0,
        0.0,
        0.0,
        100.0
    ],
    lambda r, dr, dp, sa, sb: [ # Azul
        ( dr**2 ) / ( 2*(dp**2 * r**2 + dr**2) ),
        ( dp**2 * sb * r**2 * (dr  + 2*r) ) / ( (dp**2 * r**2 + dr**2) * (dr * (sb-sa) + 2*r*(sa+sb)) ),
        ( dr**2 ) / ( 2*(dp**2 * r**2 + dr**2) ),
        ( dp**2 * sa * r**2 * (-dr + 2*r) ) / ( (dp**2 * r**2 + dr**2) * (dr * (sb-sa) + 2*r*(sa+sb)) ),
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Verde
        ( dr**2 ) / ( 2*(dp**2 * r**2 + dr**2) ),
        ( dp**2 * sa * r**2 * (dr  + 2*r) ) / ( (dp**2 * r**2 + dr**2) * (dr * (sa-sb) + 2*r*(sa+sb)) ),
        ( dr**2 ) / ( 2*(dp**2 * r**2 + dr**2) ),
        ( dp**2 * sb * r**2 * (-dr + 2*r) ) / ( (dp**2 * r**2 + dr**2) * (dr * (sa-sb) + 2*r*(sa+sb)) ),
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Rosa
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Roxo
        ( dr**2 * sa ) / ( (sa+sb) * (dp**2 * r**2 + dr**2) ),
        ( dp**2 * r * (dr  + 2*r) ) / ( 4*(dp**2 * r**2 + dr**2) ),
        ( dr**2 * sb ) / ( (sa+sb) * (dp**2 * r**2 + dr**2) ),
        ( dp**2 * r * (-dr + 2*r) ) / ( 4*(dp**2 * r**2 + dr**2) ),
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Laranja
        0.0,
        ( dp**2 * r * (dr  + 2*r) ) / ( 4*(dp**2 * r**2 + dr**2) ),
        ( dr**2 ) / ( dp**2 * r**2 + dr**2 ),
        ( dp**2 * r * (-dr + 2*r) ) / ( 4*(dp**2 * r**2 + dr**2) ),
        0.0
    ],
    lambda r, dr, dp, sa, sb: [ # Cinza
        ( dr**2 ) / ( 2*(dp**2 * r**2 + dr**2) ),
        ( dp**2 * r * (dr  + 2*r) ) / ( 4*(dp**2 * r**2 + dr**2) ),
        ( dr**2 ) / ( 2*(dp**2 * r**2 + dr**2) ),
        ( dp**2 * r * (-dr + 2*r) ) / ( 4*(dp**2 * r**2 + dr**2) ),
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

params = {
    'regions' : regions,
    'coeffs'  : coeffs,
    'initial' : initial,
    'colors'  : colors
}

materials = [5e-6, 1e-5]

r_range = [0.03, 0.11, 0.001]
phi_range = [0.0, 40.0, 1.0]

plate = Plate(r_range, phi_range, params, materials)

plate.liebmann(1.75, 0.001)

plate.plot('meshgrid')

plate.plot('voltage')
