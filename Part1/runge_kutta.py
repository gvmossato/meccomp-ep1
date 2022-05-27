import numpy as np

def RK4(F: list, x0: float, Y0: list, h: float, n: int) -> list:
    """
    Resolve um sistema de EDOs de primeira ordem pelo método
    de Runge Kutta de quarta ordem

    Args:
        F (list): funções a serem resolvidas
        x0 (float): valor inicial da variável independente
        Y0 (list): valores iniciais das variáveis dependentes
        h (foat): passo da variável independente
        n (int): número de iterações do método

    Returns:
        list: aproximações das funções na n-ésima iteração
    """
    Y = np.copy(Y0)
    x = x0

    for _ in range(n):
        K1 = h * np.array([f(x, Y) for f in F])
        K2 = h * np.array([f(x + 0.5*h, Y + 0.5*K1) for f in F])
        K3 = h * np.array([f(x + 0.5*h, Y + 0.5*K2) for f in F])
        K4 = h * np.array([f(x + h    , Y +     K3) for f in F])

        Y += (K1 + 2*K2 + 2*K3 + K4)/6
        x += h

    return Y
