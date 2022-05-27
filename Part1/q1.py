import numpy as np

from runge_kutta import RK4


global Ra, La, Rb, Lb, C, e

Ra = 200.0
La = 0.01
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


print(RK4(F, t0, Y0, h=0.001, tf=0.03))
