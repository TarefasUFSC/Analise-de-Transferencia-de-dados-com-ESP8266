import serial
import csv
import re
import argparse
import time

# Configura o parser de argumentos
parser = argparse.ArgumentParser(description='Envia o tamanho do arquivo via serial e lê o tempo de transferência.')
parser.add_argument('port', help='A porta serial do ESP. Exemplo: /dev/ttyUSB0 ou COM3.')
args = parser.parse_args()

# Abre a porta serial
ser = serial.Serial(args.port, 9600)

# Abre/cria um arquivo CSV para salvar os dados
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tamanho do Arquivo (bytes)', 'Tempo de Transferência (ms)'])  # Cabeçalho do CSV

    while True:
        # Pede ao usuário para inserir o tamanho do arquivo
        size = input("Digite o tamanho do arquivo que você deseja (em Bytes): ")

        # Envia o tamanho do arquivo via serial para o ESP
        ser.write(size.encode())
        ser.write(b'\n')  # Envia uma nova linha para indicar o final da entrada

        # Aguarda um pouco para garantir que o ESP tenha tempo para processar a entrada
        time.sleep(2)

        # Lê uma linha da saída serial
        line = ser.readline().decode('utf-8').strip()

        # Procura pelo tempo de transferência na linha lida
        time_match = re.search(r'Tempo de transferência: (\d+) ms', line)

        if time_match:
            time = time_match.group(1)

            # Escreve os dados no arquivo CSV
            writer.writerow([size, time])
            print(f"Dados salvos: Tamanho do Arquivo = {size} bytes, Tempo de Transferência = {time} ms")
