import numpy as np

from runge_kutta import RK4


Ra = 200
La = 0.01
Rb = 20
Lb = 0.5
C  = 0.002
e = lambda t: np.cos(600 * t) / La

# f1 = lambda t, Y: e(t) - q(t) / C - Ra * (i1 - i2)
# f2 = lambda t, Y: 6.0*Y[0] - Y[1]
# f3 = lambda t, y: i1 - i2

# F = np.array([f1, f2])
# Y0 = np.array([3.0, 1.0])
# x0 = 0.0

# RK4(F, x0, Y0, 0.1, 100)
