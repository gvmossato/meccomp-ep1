def validate_input(text: str, valid_inputs: list, default: str = '') -> str:
    """
    Adicona lógica de validação de entrada e valor de entrada padrão
    ao input do Python. Validações realizadas sempre com caracteres minúsculos.

    Args:
        text (str): texto a ser exibido ao solicitar input
        valid_inputs (list): lista de entradas aceitas
        default (str): entrada padrão caso o usuário não insira uma

    Returns:
        str: entrada do usuário devidamente validada
    """
    valid_inputs = [str(v) for v in valid_inputs]

    while True:
        user_input = input(text).lower() or default
        if user_input in valid_inputs: break
        print('Entrada inválida!')
    return user_input


def ctext(text: str, tag: str) -> str:
    """
    Aplica cor a uma string impressa no terminal, através de tags pré-definidas.
    As cores podem sofrer alterações conforme as configurações do terminal do usuário.

    Args:
        text (str): texto a ser colorido.
        tag (str): identificador que mapeia a cor desejada a um código
                   ASCII; tags válidas:
                   > 'r' -> Vermelho;
                   > 'g' -> Verde;
                   > 'y' -> Amarelo;
                   > 'b' -> Azul;
                   > 'm' -> Magenta;
                   > 'c' -> Ciano.

    Returns:
        str: string idêntica a text, exceto pelas tags de cor.
    """

    color_dict = {
        'r' : '\033[31m', # Red
        'g' : '\033[32m', # Green
        'y' : '\033[33m', # Yellow
        'b' : '\033[34m', # Blue
        'm' : '\033[35m', # Magenta
        'c' : '\033[36m'  # Cyan
    }

    # Aplica a tag de cor e reseta para a cor padrão do terminal do usuário.
    text = color_dict[tag] + text + '\033[0m'
    return text
