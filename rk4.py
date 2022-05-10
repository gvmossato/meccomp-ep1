import numpy as np

f1 = lambda x, Y: Y[1]
f2 = lambda x, Y: 6.0*Y[0] - Y[1]

F = np.array([f1, f2])
Y0 = np.array([3.0, 1.0])
x0 = 0.0

def rk4(F, x0, Y0, h, n):
    Y = np.copy(Y0)
    x = x0

    for _ in range(n):
        K1 = h * np.array([f(x, Y) for f in F])
        K2 = h * np.array([f(x + 0.5*h, Y + 0.5*K1) for f in F])
        K3 = h * np.array([f(x + 0.5*h, Y + 0.5*K2) for f in F])
        K4 = h * np.array([f(x + h    , Y +     K3) for f in F])

        Y += (K1 + 2*K2 + 2*K3 + K4)/6
        x += h

    print(Y)
    return Y

rk4(F, x0, Y0, 0.1, 100)