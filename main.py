
import argparse

from ExperimentWrapper import ExperimentWrapper

def get_arguments():
    """Pega os argumentos para:
        - Porta serial: String
        - Distância entre os ESPs: Float

        - Quantidade de paredes: Int (Opcional)

        - Interferência Wifi: String (Opcional) [pode ser SAME, DIFF] -> Fala se o esp e a interferencia estao na mesma ou em bandas diferentes
        - Local da Interferencia wifi: String (Opcional) [pode ser CLIENT, SERVER] -> Fala se a interferencia esta no esp cliente ou no esp servidor

        - Interferência Bluetooth: String (Opcional) [pode ser CLIENT, SERVER] -> Fala se a interferencia esta no esp cliente ou no esp servidor

        - Interferencia com Microondas: String (Opcional) [pode ser CLIENT, SERVER] -> Fala se a interferencia esta no esp cliente ou no esp servidor

        - Intereferencia com Campo Eletromagnetico: String (Opcional) [pode ser CLIENT, SERVER] -> Fala se a interferencia esta no esp cliente ou no esp servidor
    """


    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Automação dos testes de envio de dados entre os ESP8266')


    # argumento da porta conectada ao ESP
    parser.add_argument(
        '-prt',
        '--port', 
        required=True,
        help='A porta serial do ESP. Exemplo: /dev/ttyUSB0 ou COM3.'
    )

    # argumento da distancia entre os esps
    parser.add_argument(
        '-dst',
        '--distance',
        required=True,
        help='A distância entre os ESPs em metros. Exemplo: 1.5'
    )

    # argumento da quantidade de paredes
    parser.add_argument(
        '-wll',
        '--walls', 
        required=False,
        default=0,
        help='A quantidade de paredes entre os ESPs. Exemplo: 1'    
    )

    # argumento da interferencia wifi
    parser.add_argument(
        '-wfi',
        '--wifi', 
        required=False,
        default='',
        help='A interferência wifi. Exemplo: SAME ou DIFF'    
    )
    parser.add_argument(
        '-wfl',
        '--wifi_location', 
        required=False,
        default='',
        help='A localização da interferência wifi. Exemplo: CLIENT ou SERVER'    
    )

    # argumento da interferencia bluetooth
    parser.add_argument(
        '-blt',
        '--bluetooth',
        required=False,
        default='',
        help='A interferência bluetooth. Exemplo: CLIENT ou SERVER'
    )

    # argumento da interferencia com microondas
    parser.add_argument(
        '-mic',
        '--microwave',
        required=False,
        default='',
        help='A interferência com microondas. Exemplo: CLIENT ou SERVER'
    )

    # argumento da interferencia com campo eletromagnetico
    parser.add_argument(
        '-cem',
        '--electromagnetic',
        required=False,
        default='',
        help='A interferência com campo eletromagnético. Exemplo: CLIENT ou SERVER'
    )

    args = parser.parse_args()


    return args


if __name__ == "__main__":
    args = get_arguments()
    experiment = ExperimentWrapper(args)