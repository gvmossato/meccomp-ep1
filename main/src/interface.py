# ================================== #
# Intermédio entre scripts e usuário #
# ================================== #

import main.solver1 as part1
import main.solver2 as part2

from main.src.utils import validate_input, ctext


def start():
    while True:
        print("\nEscolha qual parte deseja resolver:")
        print(f"{ctext('1.', 'b')} Parte 1")
        print(f"{ctext('2.', 'b')} Parte 2")

        choosen_part = validate_input(
            f"Entre com {ctext('1', 'b')}, {ctext('2', 'b')} ou {ctext('SAIR', 'r')} para finalizar: ",
            ['1', '2', 'sair']
        )

        if choosen_part == '1':
            print("\nEscolha qual item deseja resolver:")
            print(f"{ctext('A.', 'm')} Item a)")
            print(f"{ctext('B.', 'm')} Item b1) (La = 0.1)")
            print(f"{ctext('C.', 'm')} Item b2) (Ra = 2000)")

            choosen_item = validate_input(
                f"Entre com {ctext('A', 'm')}, {ctext('B', 'm')} ou {ctext('C', 'm')}: ",
                ['a', 'b', 'c']
            )
            part1.solve(choosen_item)

        elif choosen_part == '2':
            print("\nEscolha qual item deseja resolver:")
            print(f"{ctext('A.', 'm')} Testes de discretização")
            print(f"{ctext('B.', 'm')} Solução completa com discretização adequada\n")

            choosen_item = validate_input(
                f"Entre com {ctext('A', 'm')} ou {ctext('B', 'm')}: ",
                ['a', 'b']
            )
            part2.solve(choosen_item)

        else:
            break
