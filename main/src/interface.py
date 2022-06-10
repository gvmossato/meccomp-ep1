import main.solver1 as part1
import main.solver2 as part2

from main.src.utils import validate_input, ctext


def start():
    print("Escolha qual parte deseja resolver:")
    print(f"{ctext('1.', 'b')} Parte 1")
    print(f"{ctext('2.', 'b')} Parte 2")
    choosen_part = int(validate_input(f"Entre com {ctext('1', 'b')} ou {ctext('2', 'b')}: ", [1, 2]))

    if choosen_part == 1:
        print("\nEscolha qual item deseja resolver:")
        print(f"{ctext('A.', 'm')} Item A")
        print(f"{ctext('B.', 'm')}  Item B1 (La = 0.1)")
        print(f"{ctext('C.', 'm')} Item B2 (Ra = 2000)")
        choosen_item = validate_input(f"Entre com {ctext('A', 'm')}, {ctext('B', 'm')} ou {ctext('C', 'm')}: ", ['a', 'b', 'c'])

        part1.solve(choosen_item)

    else:
        raise NotImplementedError
