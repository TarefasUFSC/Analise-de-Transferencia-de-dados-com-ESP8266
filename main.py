import serial
import csv
import re
import argparse
import time

# Configura o parser de argumentos
# argumento da porta conectada ao ESP
parser = argparse.ArgumentParser(description='Envia o tamanho do arquivo via serial e lê o tempo de transferência.')
parser.add_argument('port', help='A porta serial do ESP. Exemplo: /dev/ttyUSB0 ou COM3.')

# argumento da distancia entre os esps
parser.add_argument('distance', help='A distância entre os ESPs em metros. Exemplo: 1.5')

# argumento da quantidade de paredes
parser.add_argument('walls', help='A quantidade de paredes entre os ESPs. Exemplo: 1')

# ... assim ate ter todas as condições
args = parser.parse_args()

# Abre a porta serial
ser = serial.Serial(args.port, 9600)

print(f'Conectado à porta {args.port}, Para o teste nas seguintes condições:')
print(f'- Distância entre os ESPs: {args.distance} metros')
print(f'- Quantidade de paredes: {args.walls}')

# Abre/cria um arquivo CSV para salvar os dados
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['QTD_Bytes', 'Tempo_ms', 'Distancia_m', 'QTD_Paredes'])

    while True:
        # Pede ao usuário para inserir o tamanho do arquivo
        size = input("Digite o tamanho do arquivo que você deseja (em Bytes): ")
        
        if not size.isdigit():
            print("Digite um valor válido.")
            continue

        # Envia o tamanho do arquivo via serial para o ESP
        ser.write(size.encode())
        ser.write(b'\n') # Envia uma nova linha para indicar o final da entrada

        # Aguarda um pouco para garantir que o ESP tenha tempo para processar a entrada
        time.sleep(2)

        # Lê uma linha da saída serial
        line = ser.readline().decode('utf-8').strip()

        # Procura pelo tempo de transferência na linha lida
        time_match = re.search(r'Tempo de transferência: (\d+) ms', line)

        if time_match:
            time = time_match.group(1)

            # Escreve os dados no arquivo CSV
            writer.writerow([size, time, args.distance, args.walls])
            print(f"Dados salvos: Tamanho do Arquivo = {size} bytes, Tempo de Transferência = {time} ms")
