import serial
import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import re

class ESPSerial():
    def __init__(self, port):
        """Construtor da classe ESP_Serial"""
        self.port = port
        self._open_serial()
    
    def _open_serial(self):
        """Abre a porta serial"""
        self.serial = serial.Serial(self.port, 9600)
    
    def _close_serial(self):
        """Fecha a porta serial"""
        self.serial.close()
    
    def aguardar_substring(self, substring):
        while True:
            line = str(self.serial.readline())
            print(line)
            if substring in line:
                print(f'Achei {substring}')
                return line
            else:
                print(f'Não achei {substring}')
    
    def run_experiment(self):
        """Executa o experimento e retorna os tempo de transferência
        return [int]
        para cada tamanho é feito 3 envios
        """

        # tamanho dos arquivos: começa em 128 e vai de 128 em 128 até 10240
        sizes = [i for i in range(128, 1025, 128)]

        # data: {size: [time1, time2, time3]}
        # exemplo: {128: [1,2,3], 256: [4,5,6]}
        data = {}
        print(sizes)

        try:
            self.aguardar_substring("CONNECTED")
            time.sleep(2)
            for size in sizes:
                times = []
                for _ in range(3):  # Faz 3 envios para cada tamanho de arquivo
                    # Envia o tamanho do arquivo via serial para o ESP                    
                    # self.aguardar_substring("FILE SIZE")
                    self.serial.write(f"{size}\n".encode())
                    
                    # Aguarda um pouco para garantir que o ESP tenha tempo para processar a entrada
                    time.sleep(2)
                    
                    # fica lendo linhas ate uma delas conter a palavra SUCCESS
                    line = self.aguardar_substring("SUCCESS")
                        
                    # Procura pelo tempo de transferência na linha lida
                    time_match = re.search(r'Duration:(\d+) ms', line)
                    if time_match:
                        times.append(int(time_match.group(1)))
                        print(f"O tempo foi de: {time_match.group(1)}")
                    else:
                        print("n achei o tempo")
                    time.sleep(2)                                  
                
                data[size] = times
                print(data)

        except Exception as e:
            print(f"Ocorreu um erro durante o experimento: {e}")
            return None

        return data


if (__name__ == '__main__'):
    # Exemplo de uso
    esp_serial = ESPSerial('COM3')  # Substitua 'COM3' pela porta serial do seu ESP8266
    data = esp_serial.run_experiment()
    esp_serial._close_serial()

    if data is not None:
        print(data)
    else:
        print("Experimento não foi concluído com sucesso.")

# # Abre a porta serial
# ser = serial.Serial(args.port, 9600)



# for size in range(6912,7200,128):
#     # Pede ao usuário para inserir o tamanho do arquivo
#     # size = input("Digite o tamanho do arquivo que você deseja (em Bytes): ")
    
#     # if not size.isdigit():
#     #     print("Digite um valor válido.")
#     #     continue

#     # Envia o tamanho do arquivo via serial para o ESP
#     size = str(size)
#     ser.write(size.encode())
#     ser.write(b'\n') # Envia uma nova linha para indicar o final da entrada

#     # Aguarda um pouco para garantir que o ESP tenha tempo para processar a entrada
#     time.sleep(2)


#     # fica lendo a saida do serial
#     while(1):
#         line = str(ser.readline())
#         print(line)

#         # Procura pelo tempo de transferência na linha lida
#         time_match = re.search(r'(\d+) ms', line)
#         if(time_match):
#             print(f"O tempo foi de: {time_match}")
#             break

#     if time_match:
#         time_value = time_match.group(1)

#         # Escreve os dados no arquivo CSV
#         df = pd.read_csv('data.csv', index_col=False)
#         tam_bytes = df['QTD_Bytes'].to_list()
#         tempo_ms = df['Tempo_ms'].to_list()
#         dist_m = df['Distancia_m'].to_list()
#         qtd_paredes = df['QTD_Paredes'].to_list()

#         tam_bytes.append(size)
#         tempo_ms.append(time_value)
#         dist_m.append(args.distance)
#         qtd_paredes.append(args.walls)

#         ndf = pd.DataFrame()
#         ndf['QTD_Bytes']= np.array(tam_bytes)
#         ndf['Tempo_ms'] = np.array(tempo_ms )
#         ndf['Distancia_m'] = np.array(dist_m )
#         ndf['QTD_Paredes'] = np.array(qtd_paredes )

#         ndf.to_csv('data.csv', index=False)
#         print(f"Dados salvos: Tamanho do Arquivo = {size} bytes, Tempo de Transferência = {time_value} ms")

# df = pd.read_csv('data.csv', index_col=False)


# plt.plot(df['QTD_Bytes'], df['Tempo_ms'])
# plt.show()