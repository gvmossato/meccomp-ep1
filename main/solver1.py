import numpy as np

from src.lib1 import RK4, scale_plot


global Ra, La, Rb, Lb, C, e

def solve(item: str):
    Ra = 200.0 if (item in ['a', 'b']) else 2000
    La = 0.01 if (item in ['a', 'c']) else 0.1
    Rb = 20.0
    Lb = 0.5
    C  = 0.002
    e  = lambda t: np.cos(600 * t) / La

    Y0 = [0.0, 0.0, 0.0] # Y = [i1, i2, q]

    f1 = lambda t, Y: ( e(t) - Y[2]/C - Ra*(Y[0]-Y[1]) ) / La
    f2 = lambda t, Y: ( Y[2]/C + Ra*(Y[0]-Y[1]) - Rb*Y[1] ) / Lb
    f3 = lambda t, Y: Y[0] - Y[1]

    F = [f1, f2, f3]

    t0 = 0.0

    steps = [1e-6, 1e-3, 1e-2] if (item == 'a') else [1e-6]

    for h in steps:
        T, Y_hist, K1_hist = RK4(F, t0, Y0, h, tf=0.03)

        Y = np.vstack([Y_hist, K1_hist[0:2]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {h}",
            ylabel = "Corrente e Carga (SI × 10^x)",
            xlabel = "Tempo (s)",
            legend = ['i₁', 'i₂', 'q', 'di₁/dt', 'di₂/dt']
        )
    return
