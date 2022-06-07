import scripts.part1 as part1

from src.utils import validate_input


def start():
    print("Escolha qual parte deseja resolver:")
    print("1. Parte 1")
    print("2. Parte 2")
    choosen_part = int(validate_input("Entre com 1 ou 2: ", [1, 2]))

    if choosen_part == 1:
        print("Escolha qual item deseja resolver:")
        print('a. Item A')
        print('b. Item B1 (La = 0.1)')
        print('c. Item B2 (Ra = 2000)')
        choosen_item = validate_input("Entre com A, B ou C: ", ['a', 'b', 'c'])

        part1.solve(choosen_item)

    else:
        raise NotImplementedError
