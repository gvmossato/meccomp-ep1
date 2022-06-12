# ============================== #
# Script para solução da Parte 2 #
# ============================== #

from main.src.utils import ctext, validate_input
from main.src.params import params
from main.src.lib2 import Plate


def solve(item):
    if item == 'a':
        r_ranges = [
            [0.03, 0.11, 0.010],
            [0.03, 0.11, 0.005],
            [0.03, 0.11, 0.001]
        ]
        phi_ranges = [
            [0.0, 40.0, 2.0],
            [0.0, 40.0, 1.0],
            [0.0, 40.0, 0.5],
        ]
    else:
        r_ranges   = [[0.03, 0.11, 0.001]]
        phi_ranges = [[0.00, 40.0, 1.000]]

    props = {
        'sa'   : 5e-6,
        'sb'   : 1e-5,
        'ka'   : 110.0,
        'kb'   : 500.0,
        'Tamb' : 298.0,
        'h'    : 50.0
    }

    for r_range, phi_range in zip(r_ranges, phi_ranges):
        print('\033[F', end='')
        print("Gerando nova malha...              ")
        print(ctext(f"Passos: ({r_range[-1]}, {phi_range[-1]})", 'm'))

        plate = Plate(r_range, phi_range, params, props)


        print(f"\n{ctext('Meshgrids inicializadas!', 'g')}")

        while True:
            print(f"\nDeseja plotar alguma mesh?")
            print(f"{ctext('M.', 'c')} Distribuição dos diferentes materiais")
            print(f"{ctext('V.', 'c')} Contornos para tensão")
            print(f"{ctext('T.', 'c')} Contornos para temperatura")
            print(f"{ctext('R.', 'c')} Contornos para densidade de corrente e fluxo de calor (coordenada radial)")
            print(f"{ctext('P.', 'c')} Contornos para densidade de corrente e fluxo de calor (coordenada angular)")

            choosen_meshgrid = validate_input(
                f"Entre com {ctext('M', 'c')}, {ctext('V', 'c')}, {ctext('T', 'c')}, {ctext('R', 'c')}, {ctext('P', 'c')} ou pressione {ctext('ENTER', 'g')} para continuar: ",
                ['m', 'v', 't', 'r', 'p', 'ENTER'],
                'ENTER'
            )
            if choosen_meshgrid in ['m', 'v', 't']: choosen_meshgrid = choosen_meshgrid.upper()
            elif choosen_meshgrid == 'r': choosen_meshgrid = 'Jr'
            elif choosen_meshgrid == 'p': choosen_meshgrid = 'Jphi'
            else: break
            plate.plot_meshgrid(choosen_meshgrid)

        print('\nCalculando e plotando a distribuição de tensão:')
        plate.apply_liebmann_for('V', 1.75, 0.0001)
        plate.plot('V')

        if item == 'a':
            input(f"\nPressione {ctext('ENTER', 'g')} para continuar\r")

    if item == 'a':
        return

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando e plotando a densidade de corrente...')
    plate.calculate_flux('J')
    plate.plot('J')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    plate.calculate('i')
    plate.calculate('R')
    print('\033[F', end='')
    print('Propriedades do bloco encontradas:')
    print(f"{ctext('Corrente através da parede:', 'b')} {plate.i*1000:.4} mA")
    print(f"{ctext('Resistência:', 'b')} {plate.R/1000:.4} kΩ")

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando e plotando a fonte de calor distribuído...')
    plate.calculate('dot_q')
    plate.plot('dot_q')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar\r")

    print('\033[F', end='')
    print('Calculando e plotando a distribuição de temperatura...')
    plate.apply_liebmann_for('T', 1.75, 0.0001)
    plate.plot('T')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar\r")

    print('\033[F', end='')
    print('Calculando e plotando o fluxo de calor...')
    plate.calculate_flux('Q')
    plate.plot('Q')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar\r")

    print('\033[F', end='')
    plate.calculate('q_conv')
    print('Propriedade encontrada:')
    print(f"{ctext('Perda de calor por convecção:', 'b')} {plate.q_conv*1000:.4} mW/m²")
    return
